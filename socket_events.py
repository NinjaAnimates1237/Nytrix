from flask import request
from flask_socketio import emit, join_room, leave_room
from flask_jwt_extended import decode_token
from app import socketio, db
from models import User, Message

online_users = {}

@socketio.on('connect')
def handle_connect(auth):
    try:
        token = auth.get('token')
        if not token:
            return False
        
        decoded = decode_token(token)
        user_id = int(decoded['sub'])
        
        online_users[user_id] = request.sid
        
        # Update user status
        user = User.query.get(user_id)
        if user:
            user.status = 'online'
            db.session.commit()
            
            # Broadcast status
            emit('user_status', {'userId': user_id, 'status': 'online'}, broadcast=True)
        
        print(f'User {user_id} connected')
        return True
    except Exception as e:
        print(f'Connection error: {e}')
        return False

@socketio.on('disconnect')
def handle_disconnect():
    user_id = None
    for uid, sid in online_users.items():
        if sid == request.sid:
            user_id = uid
            break
    
    if user_id:
        del online_users[user_id]
        
        # Update user status
        user = User.query.get(user_id)
        if user:
            user.status = 'offline'
            db.session.commit()
            
            # Broadcast status
            emit('user_status', {'userId': user_id, 'status': 'offline'}, broadcast=True)
        
        print(f'User {user_id} disconnected')

@socketio.on('join_channel')
def handle_join_channel(data):
    channel_id = data.get('channelId')
    join_room(f'channel_{channel_id}')
    print(f'User joined channel {channel_id}')

@socketio.on('leave_channel')
def handle_leave_channel(data):
    channel_id = data.get('channelId')
    leave_room(f'channel_{channel_id}')
    print(f'User left channel {channel_id}')

@socketio.on('send_channel_message')
def handle_channel_message(data):
    try:
        # Get user from session
        user_id = None
        for uid, sid in online_users.items():
            if sid == request.sid:
                user_id = uid
                break
        
        if not user_id:
            emit('error', {'message': 'Unauthorized'})
            return
        
        channel_id = data.get('channelId')
        content = data.get('content')
        
        message = Message(
            sender_id=user_id,
            content=content,
            channel_id=channel_id,
            is_direct_message=False
        )
        
        db.session.add(message)
        db.session.commit()
        
        # Broadcast to channel
        emit('channel_message', message.to_dict(), room=f'channel_{channel_id}')
    except Exception as e:
        print(f'Channel message error: {e}')
        emit('error', {'message': 'Failed to send message'})

@socketio.on('send_dm')
def handle_direct_message(data):
    try:
        # Get user from session
        user_id = None
        for uid, sid in online_users.items():
            if sid == request.sid:
                user_id = uid
                break
        
        if not user_id:
            emit('error', {'message': 'Unauthorized'})
            return
        
        recipient_id = data.get('recipientId')
        content = data.get('content')
        
        message = Message(
            sender_id=user_id,
            content=content,
            recipient_id=recipient_id,
            is_direct_message=True
        )
        
        db.session.add(message)
        db.session.commit()
        
        # Send to recipient if online
        if recipient_id in online_users:
            emit('dm_message', message.to_dict(), room=online_users[recipient_id])
        
        # Send back to sender
        emit('dm_message', message.to_dict())
    except Exception as e:
        print(f'DM error: {e}')
        emit('error', {'message': 'Failed to send message'})

@socketio.on('typing')
def handle_typing(data):
    user_id = None
    for uid, sid in online_users.items():
        if sid == request.sid:
            user_id = uid
            break
    
    if not user_id:
        return
    
    channel_id = data.get('channelId')
    recipient_id = data.get('recipientId')
    
    if channel_id:
        emit('user_typing', {'userId': user_id, 'channelId': channel_id}, 
             room=f'channel_{channel_id}', include_self=False)
    elif recipient_id and recipient_id in online_users:
        emit('user_typing', {'userId': user_id}, room=online_users[recipient_id])

@socketio.on('stop_typing')
def handle_stop_typing(data):
    user_id = None
    for uid, sid in online_users.items():
        if sid == request.sid:
            user_id = uid
            break
    
    if not user_id:
        return
    
    channel_id = data.get('channelId')
    recipient_id = data.get('recipientId')
    
    if channel_id:
        emit('user_stop_typing', {'userId': user_id, 'channelId': channel_id}, 
             room=f'channel_{channel_id}', include_self=False)
    elif recipient_id and recipient_id in online_users:
        emit('user_stop_typing', {'userId': user_id}, room=online_users[recipient_id])

@socketio.on('friend_request')
def handle_friend_request(data):
    recipient_id = data.get('recipientId')
    if recipient_id in online_users:
        emit('friend_request_received', data, room=online_users[recipient_id])
