from argparse import ArgumentParser
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import aws_client
import rekognition_api as rekognition
import image_processing as image_processing
from pprint import pprint as pp

def get_args():
    parser = ArgumentParser(description='AWS Rekognition Client')
    parser.add_argument('-a', '--action', help='Call to be performed', required=True)
    parser.add_argument('-t', '--target_image')
    parser.add_argument('-s', '--source_image')
    parser.add_argument('-d', '--source_directory')
    parser.add_argument('-c', '--collection_id')
    parser.add_argument('-f', '--face_id')
    parser.add_argument('-x', '--external_image_id')
    parser.add_argument('-z', '--confidence_threshold', type=float, default=80.0)
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    client = aws_client.get_client('rekognition', verify=True)

    res = None
    # Collections =================================================================
    if args.action in ['list_collections', 'lc']:
        res = rekognition.list_collections(client)
    elif args.action in ['create_collection', 'cc']:
        if args.collection_id:
            res = rekognition.create_collection(client, args.collection_id)
    elif args.action in ['delete_collection', 'dc']:
        if args.collection_id:
            res = rekognition.delete_collection(client, args.collection_id)
    # Faces =======================================================================
    elif args.action in ['index_faces', 'if']:
        if args.collection_id and args.source_image:
            res = rekognition.index_faces(client, args.source_image, args.collection_id,
                                          external_image_id=args.external_image_id)
    elif args.action in ['index_faces_directory', 'ifd']:
        if args.collection_id and args.source_directory:
            res = rekognition.index_faces_directory(client, args.source_directory, args.collection_id,
                                                    external_image_id=args.external_image_id)
    elif args.action in ['delete_faces', 'df']:
        if args.collection_id and args.face_id:
            res = rekognition.delete_faces(client, [args.face_id], args.collection_id)
    elif args.action in ['delete_faces_by_external_image_id', 'dfe']:
        if args.collection_id and args.external_image_id:
            res = rekognition.delete_faces(client, args.external_image_id, args.collection_id)
    elif args.action in ['list_faces', 'lf']:
        if args.collection_id:
            res = rekognition.list_faces(client, args.collection_id)
    # Non-storage operations ======================================================
    elif args.action in ['detect_faces', 'dtf']:
        if args.source_image:
            res = rekognition.detect_faces(client, args.source_image)
    elif args.action in ['detect_labels', 'dtl']:
        if args.source_image:
            res = rekognition.detect_labels(client, args.source_image,
                                            min_confidence=args.confidence_threshold)
    elif args.action in ['compare_faces', 'cpf']:
        if args.source_image and args.target_image:
            res = rekognition.compare_faces(client, args.source_image, args.target_image,
                                            similarity_threshold=args.confidence_threshold)
    # Storage operations ===========================================================
    elif args.action in ['search_faces', 'sf']:
        if args.collection_id and args.face_id:
            res = rekognition.search_faces(client, args.face_id, args.collection_id,
                                           face_match_threshold=args.confidence_threshold)
    elif args.action in ['search_faces_by_image', 'sfi']:
        if args.collection_id and args.source_image:
            res = rekognition.search_faces_by_image(client, args.source_image, args.collection_id,
                                                    face_match_threshold=args.confidence_threshold)
    # Custom operations ======================================================
    elif args.action in ['search_all_faces_by_image', 'saf']:
        if args.collection_id and args.source_image:
            res = rekognition.search_all_faces_by_image(client, args.source_image, args.collection_id,
                                                        face_match_threshold=args.confidence_threshold)
