from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource,reqparse,abort,fields,marshal_with

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///exe.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONs'] = False
db = SQLAlchemy(app)
api = Api(app)


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)

    def __init__(self, username):
        self.username = username

user_args = reqparse.RequestParser()
user_args.add_argument('username', type=str, required=True, help='Username is required')
userFields = {'id':fields.Integer,'username':fields.String}


class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users

    @marshal_with(userFields)    
    def post(self):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(username=args['username']).first()
        if user:
            return abort(409,message='User already exists')
       
        new_user = UserModel(username=args['username'])
        db.session.add(new_user)
        db.session.commit()
        users = UserModel.query.all()
        return users
    
class User(Resource):
    @marshal_with(userFields)
    def get(self,id):
        user = UserModel.query.get(id)
        if not user:
            return abort(404, message='User not found')
        return user
    
    @marshal_with(userFields)
    def patch(self,id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            return abort(404, message='User not found')
        user.username = args['username']
        db.session.commit()
        return user
    
    @marshal_with(userFields)
    def delete(self,id):
        user = UserModel.query.get(id)
        if not user:
            return abort(404,message='User not found')
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()


api.add_resource(Users,'/users/')
api.add_resource(User,'/users/<int:id>')

@app.route('/')
def home():
    return "Hello, World!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5001, debug=True)