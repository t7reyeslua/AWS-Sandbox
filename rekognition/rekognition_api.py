from pprint import pprint as pp

# COLLECTIONS MANAGEMENT ==================================================================================
def create_collection(client, collection_id):
    print('%s.create_collection: %s' % (client.api_name, collection_id))
    response = client.api.create_collection(CollectionId=collection_id)
    pp(response)
    return response


def delete_collection(client, collection_id):
    print('%s.delete_collection: %s' % (client.api_name, collection_id))
    response = client.api.delete_collection(CollectionId=collection_id)
    pp(response)
    return response


def list_collections(client, max_results=100):
    print('%s.list_collections' % (client.api_name))
    collections = []
    response = client.api.list_collections(MaxResults=max_results)
    pp(response)
    collections.extend(response.get('CollectionIds', []))

    if response.get('NextToken', None) is not None:
        # Results are paginated
        more_results = True
        while more_results:
            next_token = response['NextToken']
            response = client.api.list_collections(MaxResults=max_results, NextToken=next_token)
            pp(response)
            collections.extend(response.get('CollectionIds', []))
            if response.get('NextToken', None) is None:
                more_results = False
    return collections


# FACES MANAGEMENT =======================================================================================
def index_faces(client, image_url, collection_id, external_image_id=None):
    print('%s.index_faces of image %s in collection: %s' % (client.api_name, image_url, collection_id))
    response = None
    with open(image_url, 'rb') as image:
        if external_image_id is None:
            response = client.api.index_faces(Image={'Bytes': image.read()}, CollectionId=collection_id)
        else:
            response = client.api.index_faces(Image={'Bytes': image.read()}, CollectionId=collection_id,
                                              ExternalImageId=external_image_id)
        pp(response)
    return response


def delete_faces(client, face_ids, collection_id):
    print('%s.delete_faces %s in collection: %s' % (client.api_name, face_ids, collection_id))
    response = client.api.delete_faces(CollectionId=collection_id, FaceIds=face_ids)
    pp(response)
    return response


def list_faces(client, collection_id, max_results=100):
    print('%s.list_faces in collection: %s' % (client.api_name, collection_id))
    faces = []
    response = client.api.list_faces(CollectionId=collection_id, MaxResults=max_results)
    pp(response)
    faces.extend(response.get('Faces', []))

    if response.get('NextToken', None) is not None:
        # Results are paginated
        more_results = True
        while more_results:
            next_token = response['NextToken']
            response = client.api.list_faces(CollectionId=collection_id, MaxResults=max_results, NextToken=next_token)
            pp(response)
            faces.extend(response.get('Faces', []))
            if response.get('NextToken', None) is None:
                more_results = False
    return faces

# NON-STORAGE IMAGE OPERATIONS ===========================================================================
def detect_faces(client, image_url, attributes=None):
    print('%s.detect_faces of image: %s' % (client.api_name, image_url))
    response = None
    if attributes is None:
        attributes = ['ALL']
    with open(image_url, 'rb') as image:
        response = client.api.detect_faces(Image={'Bytes': image.read()}, Attributes=attributes)
        pp(response)
    return response


def detect_labels(client, image_url, min_confidence=50.0):
    print('%s.detect_labels of image: %s' % (client.api_name, image_url))
    response = None
    with open(image_url, 'rb') as image:
        response = client.api.detect_labels(Image={'Bytes': image.read()}, MinConfidence=min_confidence)
        pp(response)
    return response


def compare_faces(client, source_image_url, target_image_url, similarity_threshold=80.0):
    print('%s.compare_faces of source %s and target %s' % (client.api_name, source_image_url, target_image_url))
    response = None
    with open(source_image_url, 'rb') as source_image, open(target_image_url, 'rb') as target_image:
        response = client.api.compare_faces(SourceImage={'Bytes': source_image.read()},
                                            TargetImage={'Bytes': target_image.read()},
                                            SimilarityThreshold=similarity_threshold)
        pp(response)
    return response

# STORAGE IMAGE OPERATIONS ===============================================================================
def search_faces(client, face_id, collection_id, max_faces=10, face_match_threshold=80.0):
    print('%s.search_faces of face: %s' % (client.api_name, face_id))
    response = client.api.search_faces_by_image(
        FaceId=face_id,
        CollectionId=collection_id,
        MaxFaces=max_faces,
        FaceMatchThreshold=face_match_threshold)
    pp(response)
    return response

def search_faces_by_image(client, image_url, collection_id, max_faces=10, face_match_threshold=80.0):
    print('%s.search_faces_by_image of image: %s' % (client.api_name, image_url))
    response = None
    with open(image_url, 'rb') as image:
        response = client.api.search_faces_by_image(
            Image={'Bytes': image.read()},
            CollectionId=collection_id,
            MaxFaces=max_faces,
            FaceMatchThreshold=face_match_threshold)
        pp(response)
    return response