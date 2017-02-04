"""

This file is the place to write solutions for the
skills assignment called skills-sqlalchemy. Remember to
consult the exercise instructions for more complete
explanations of the assignment.

All classes from model.py are being imported for you
here, so feel free to refer to classes without the
[model.]User prefix.

"""

from model import *

init_app()


# -------------------------------------------------------------------
# Part 2: Discussion Questions


# 1. What is the datatype of the returned value of
# ``Brand.query.filter_by(name='Ford')``?

# It returns an object because the .all(), .first(), .one(), is the part that 
# actually returns the query that one is probably looking for 

# 2. In your own words, what is an association table, and what type of
# relationship (many to one, many to many, one to one, etc.) does an
# association table manage?


# An association table is a go between table of two tables that have a many to many
# relationship that holds foreign keys to both tables, generally you could think
# of each individual transaction between the two tables as being held as a
# seperate column in the association table (for example each individual comment
# or each genre interaction with a book). If it contains other important information
# that is not just the relations between the two tables is generally known as a
# middle table. 



# -------------------------------------------------------------------
# Part 3: SQLAlchemy Queries


# Get the brand with the ``id`` of "ram."
q1 = Brand.query.filter_by(brand_id='ram').one()

# Get all models with the name "Corvette" and the brand_id "che."
q2 = Model.query.filter_by(name='Corvette').filter_by(brand_id='che').all()

# Get all models that are older than 1960.
q3 =  Model.query.filter(Model.year > 1960).all()

# Get all brands that were founded after 1920.
q4 = Brand.query.filter(Brand.founded > 1920).all()

# Get all models with names that begin with "Cor."
q5 = Model.query.filter(Model.name.like('Cor%')).all()

# Get all brands that were founded in 1903 and that are not yet discontinued.
q6 = Brand.query.filter_by(founded=1903).filter(Brand.discontinued == None).all()

# Get all brands that are either 1) discontinued (at any time) or 2) founded
# before 1950.
q7 = Brand.query.filter((Brand.discontinued != None) | (Brand.founded < 1950)).all()

# Get any model whose brand_id is not "for."
q8 = Model.query.filter(Model.brand_id != 'for').all()



# -------------------------------------------------------------------
# Part 4: Write Functions


def get_model_info(year):
    """Takes in a year and prints out each model name, brand name, and brand
    headquarters for that year using only ONE database query."""

    models = db.session.query(Model.name, 
                                  Brand.name,
                                  Brand.headquarters).join(Brand).filter(Model.year == 1960).all()


    for model in models:
        print model[0], model[1], model[2]


def get_brands_summary():
    """Prints out each brand name and each model name with year for that brand
    using only ONE database query."""


    brands = Brand.query.options(db.joinedload('models')).all()

    brand_models = {}

    for brand in brands:
        brand_name = brand.name
        brand_models[brand_name] = []
        for model in brand.models:
            model_name = model.name
            year = model.year
            brand_models[brand_name].append((model_name, year))

    for key, value in brand_models.items():
        print '%s:' %(key)
        for model in value:
            print "\t%s(%s)" % (model[0], model[1])
        print



def search_brands_by_name(mystr):
    """Returns all Brand objects corresponding to brands whose names include
    the given string."""

    return Brand.query.filter(Brand.name.like('%'+mystr+'%')).all()



def get_models_between(start_year, end_year):
    """Returns all Model objects corresponding to models made between
    start_year (inclusive) and end_year (exclusive)."""

    return Model.query.filter(Model.year >= start_year, Model.year < end_year).all()

