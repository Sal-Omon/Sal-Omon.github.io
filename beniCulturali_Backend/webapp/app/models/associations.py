from app.extensions import db

#many to many association table
artifact_materials = db.Table(
    'artifact_material', #db table name
    db.Column('artifact_id', db.Integer, db.ForeignKey('artifacts.id'), primary_key=True),
    db.Column('material_id', db.Integer, db.ForeignKey('materials.material_id'), primary_key=True)
)

artifact_tags = db.Table(
    'artifact_tags',
    db.Column('artifact_id', db.Integer, db.ForeignKey('artifacts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.tag_id'), primary_key=True)
)

artifact_creators = db.Table(
    'artifact_creator',
    db.Column('artifact_id', db.Integer, db.ForeignKey('artifacts.id'), primary_key=True),
    db.Column('creator_id', db.Integer, db.ForeignKey('creators.creator_id'), primary_key=True)
)

#un record in un table può collegarsi a piu record nell altro table
#the tables exists solely to store the foreign keys