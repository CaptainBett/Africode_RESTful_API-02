from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource,reqparse,marshal_with,fields,abort
from datetime import datetime,timezone

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class UserModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(30),unique=True,nullable=False)
    posts = db.relationship('PostModel', backref='author', lazy=True)

    def __repr__(self):
        return {self.username}
    

class PostModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    created_at = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)

    def __repr__(self):
        return {self.title}



user_args = reqparse.RequestParser()
user_args.add_argument('username',type=str,required=True,help='Username is required')

userFields = {"id":fields.Integer,"username":fields.String}
#postFields = {"id":fields.Integer,"title":fields.String,"content":fields.String,"created_at":fields.DateTime,"user_id":fields.Integer}
    
class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users, 200
    
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        new_user = UserModel(username=args['username'])
        db.session.add(new_user)
        db.session.commit()
        return new_user, 201



class User(Resource):
    @marshal_with(userFields)
    def get(self,id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404,message=f"User with id {id} not found") 
        return user, 200

    @marshal_with(userFields)   
    def patch(self,id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message=f"User with id {id} not found")
        user.username = args['username']
        db.session.commit()
        return user, 200
    
    @marshal_with(userFields) 
    def delete(self,id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message=f"User with id {id} not found")
        
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users
    

class Posts(Resource):
    # @marshal_with(postFields)
    def get(self):
        posts = PostModel.query.all()
        return posts, 200

api.add_resource(Users,'/api/users/')
api.add_resource(User, '/api/users/<int:id>')
api.add_resource(Posts,'/api/posts/')



@app.route('/')
def home():
    return "Hello world!"



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
 