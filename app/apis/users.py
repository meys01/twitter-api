from flask_restplus import Namespace, Resource, fields
from flask import abort
from app import db
from app.models import User

api = Namespace('users')

json_user = api.model('User', {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'api_key': fields.String
})

json_new_user = api.model('New user', {
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'api_key': fields.String(required=True)
})

json_update_user = api.model('Update user', {
    'username': fields.String,
    'email': fields.String,
    'api_key': fields.String
})

@api.route('/')
class TweetResource(Resource):
    @api.marshal_with(json_user)
    def get(self):
        user = db.session.query(User).all()
        if user is None:
            api.abort(404, "User {} doesn't exist".format(id))
        else:
            return user


@api.route('/<int:id>')
@api.response(404, 'user not found')
@api.param('id', 'The user unique identifier')
class TweetResource(Resource):
    @api.marshal_with(json_user)
    def get(self, id):
        user = db.session.query(User).get(id)
        if user is None:
            api.abort(404, "user {} doesn't exist".format(id))
        else:
            return user

    @api.marshal_with(json_user, code=200)
    @api.expect(json_update_user, validate=True)
    def patch(self, id):
        user = db.session.query(User).get(id)
        keys = ["username", "email", "api_key"]
        if user is None:
            api.abort(404, "User {} doesn't exist".format(id))
        for key in keys:
            if key in api.payload:
                setattr(user, key, api.payload[key])
        db.session.commit()
        return user

    def delete(self, id):
        user = db.session.query(Tweet).get(id)
        if user is None:
            api.abort(404, "User {} doesn't exist".format(id))
        else:
            db.session.delete(user)
            db.session.commit()
            return None

@api.route('')
@api.response(422, 'Invalid user')
class TweetsResource(Resource):
    @api.marshal_with(json_user, code=201)
    @api.expect(json_new_user, validate=True)
    def post(self):
        keys = ["username", "email", "api_key"]
        username = api.payload["username"]
        email = api.payload["email"]
        api_key = api.payload["api_key"]
        user = User(username=username, email=email, api_key=api_key)
        db.session.add(user)
        db.session.commit()
        return user, 201

