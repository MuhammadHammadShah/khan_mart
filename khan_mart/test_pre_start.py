from sqlmodel import SQLModel 

from sqlalchemy import Engine 
from khan_mart.core.db_settings import engine
from khan_mart.core.logging import logConfig
from sqlmodel import Session


logger=logConfig(__name__)

def createTable(*,engine:Engine):
    
    logger.info("Creating Table ....")
    try :    
      SQLModel.metadata.create_all(engine)
    except Exception as e:
        logger.error(e)
        raise e
    
    
def init_test_db(* ,engine:Engine):
    
    try:
        
        logger.info("Create The Table")    
        
        createTable(engine=engine)
        
        # logger.info("Start Seeding the database")
        
        ...
        
                
    except Exception as e:
        logger.error(f"{e}")
        raise e    
    
def main()->None:
    
    
    logger.info("Initializing The Services")
    
    with Session(engine) as session:
        init_test_db(engine=engine)
        
        
        
        
    
    
        
    # createTable(engine=engine)    
    
if __name__ =="__main__":

    main()
    