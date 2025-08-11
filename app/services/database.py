import os
from typing import Dict, List, Optional
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from datetime import datetime, timezone

class DatabaseService:
    """Service for MongoDB database operations."""
    
    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None
        self.connect()
    
    def connect(self):
        """Connect to MongoDB database."""
        try:
            mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
            db_name = os.getenv("MONGODB_DB_NAME", "whatsapp_agent_system")
            
            self.client = MongoClient(mongo_uri)
            self.db = self.client[db_name]
            
            # Test connection
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB")
            
        except Exception as e:
            print(f"Failed to connect to MongoDB: {str(e)}")
            self.client = None
            self.db = None
    
    def get_collection(self, collection_name: str) -> Optional[Collection]:
        """Get a MongoDB collection."""
        if self.db is not None:
            return self.db[collection_name]
        return None
    
    def insert_document(self, collection_name: str, document: Dict) -> Optional[str]:
        """Insert a document into a collection."""
        try:
            collection = self.get_collection(collection_name)
            if collection is not None:
                # Only add datetime fields if they don't already exist
                if 'created_at' not in document:
                    document['created_at'] = datetime.now(timezone.utc)
                if 'updated_at' not in document:
                    document['updated_at'] = datetime.now(timezone.utc)
                result = collection.insert_one(document)
                return str(result.inserted_id)
        except Exception as e:
            print(f"Error inserting document: {str(e)}")
        return None
    
    def find_documents(self, collection_name: str, query: Dict = None, limit: int = 0) -> List[Dict]:
        """Find documents in a collection."""
        try:
            collection = self.get_collection(collection_name)
            if collection is not None:
                if query is None:
                    query = {}
                cursor = collection.find(query)
                if limit > 0:
                    cursor = cursor.limit(limit)
                documents = list(cursor)
                
                # Convert datetime objects to ISO format strings for JSON serialization
                for doc in documents:
                    for key, value in doc.items():
                        if hasattr(value, 'isoformat'):
                            doc[key] = value.isoformat()
                
                return documents
        except Exception as e:
            print(f"Error finding documents: {str(e)}")
        return []
    
    def find_document_by_id(self, collection_name: str, document_id: str) -> Optional[Dict]:
        """Find a document by its ID."""
        try:
            from bson import ObjectId
            collection = self.get_collection(collection_name)
            if collection is not None:
                # Try to find by job_id first (for UUID-style IDs)
                doc = collection.find_one({"job_id": document_id})
                if doc:
                    # Convert datetime objects to ISO format strings for JSON serialization
                    for key, value in doc.items():
                        if hasattr(value, 'isoformat'):
                            doc[key] = value.isoformat()
                    return doc
                
                # If not found by job_id, try ObjectId
                try:
                    doc = collection.find_one({"_id": ObjectId(document_id)})
                    if doc:
                        # Convert datetime objects to ISO format strings for JSON serialization
                        for key, value in doc.items():
                            if hasattr(value, 'isoformat'):
                                doc[key] = value.isoformat()
                    return doc
                except:
                    pass
        except Exception as e:
            print(f"Error finding document by ID: {str(e)}")
        return None
    
    def update_document(self, collection_name: str, document_id: str, update_data: Dict) -> bool:
        """Update a document in a collection."""
        try:
            from bson import ObjectId
            collection = self.get_collection(collection_name)
            if collection is not None:
                update_data['updated_at'] = datetime.now(timezone.utc)
                
                # Try to update by job_id first (for UUID-style IDs)
                result = collection.update_one(
                    {"job_id": document_id},
                    {"$set": update_data}
                )
                if result.modified_count > 0:
                    return True
                
                # If not found by job_id, try ObjectId
                try:
                    result = collection.update_one(
                        {"_id": ObjectId(document_id)},
                        {"$set": update_data}
                    )
                    return result.modified_count > 0
                except:
                    pass
        except Exception as e:
            print(f"Error updating document: {str(e)}")
        return False
    
    def delete_document(self, collection_name: str, document_id: str) -> bool:
        """Delete a document from a collection."""
        try:
            from bson import ObjectId
            collection = self.get_collection(collection_name)
            if collection is not None:
                result = collection.delete_one({"_id": ObjectId(document_id)})
                return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting document: {str(e)}")
        return False
    
    def create_index(self, collection_name: str, field: str, unique: bool = False):
        """Create an index on a collection field."""
        try:
            collection = self.get_collection(collection_name)
            if collection is not None:
                collection.create_index(field, unique=unique)
        except Exception as e:
            print(f"Error creating index: {str(e)}")
    
    def close(self):
        """Close the database connection."""
        if self.client is not None:
            self.client.close()

# Global database service instance
db_service = DatabaseService()
