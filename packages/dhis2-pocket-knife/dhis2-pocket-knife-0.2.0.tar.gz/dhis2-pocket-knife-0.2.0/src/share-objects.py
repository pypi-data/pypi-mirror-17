#!/usr/bin/env python

"""
share-objects
~~~~~~~~~~~~~~~~~
This script assigns sharing to shareable DHIS2 objects like userGroups and publicAccess.
"""

import argparse
import sys

from src.core.core import Dhis


class Sharer(Dhis):
    """Inherited from core Dhis class to extend functionalities"""

    def __init__(self, server, username, password):
        Dhis.__init__(self, server, username, password)

    def get_usergroup_uid(self, usergroup_name):
        """Get UID of userGroup based on userGroup.name"""

        params = {
            'fields': 'id,name',
            'paging': False,
            'filter': 'name:like:' + usergroup_name
        }

        print("Getting " + usergroup_name + " UID...")

        endpoint = "userGroups"
        response = self.get(endpoint=endpoint, params=params)

        if len(response['userGroups']) == 1:
            uid = response['userGroups'][0]['id']
            self.log.info(usergroup_name + " UID: " + uid)
            return uid
        else:
            msg = 'Failure in getting (only one) userGroup UID for filter "name:like:' + usergroup_name + '"'
            print(msg)
            self.log.info(msg)
            sys.exit()

    def get_objects(self, objects, objects_filter):
        """Returns DHIS2 filtered objects"""

        params = {
            'fields': 'id,name,code',
            'filter': [objects_filter],
            'paging': False
        }
        print("Getting " + objects + " with filter=" + objects_filter)
        response = self.get(endpoint=objects, params=params)

        if len(response[objects]) > 0:
            return response
        else:
            msg = 'No objects found. Wrong filter?'
            self.log.info(msg)
            print(msg)
            sys.exit()

    def share_object(self, payload, parameters):
        """Share object by using sharing enpoint"""
        self.post(endpoint="sharing", params=parameters, payload=payload)


# argument parsing
parser = argparse.ArgumentParser(description="Share DHIS2 objects (dataElements, programs, ...) with userGroups")
parser.add_argument('-s', '--server', action='store', required=True,
                    help='DHIS2 server, e.g. "play.dhis2.org/demo"')
parser.add_argument('-t', '--object_type', action='store', required=True, choices=Dhis.objects_types,
                    help='DHIS2 objects to apply sharing')
parser.add_argument('-f', '--filter', action='store', required=True,
                    help='Filter on object name according to DHIS2 field filter')
parser.add_argument('-w', '--usergroup_readwrite', action='store', required=False,
                    help='UserGroup Name with Read-Write rights')
parser.add_argument('-r', '--usergroup_readonly', action='store', required=False,
                    help='UserGroup Name with Read-Only rights')
parser.add_argument('-a', '--publicaccess', action='store', required=True, choices=Dhis.public_access.keys(),
                    help='publicAccess (with login)')
parser.add_argument('-u', '--username', action='store', required=True, help='DHIS2 username')
parser.add_argument('-p', '--password', action='store', required=True, help='DHIS2 password')
args = parser.parse_args()

# init DHIS
dhis = Sharer(args.server, args.username, args.password)

# get UID of usergroup with RW access
readwrite_usergroup_uid = dhis.get_usergroup_uid(args.usergroup_readwrite)

# get UID of usergroup with RO access
readonly_usergroup_uid = dhis.get_usergroup_uid(args.usergroup_readonly)

# pull objects for which to apply sharing
data = dhis.get_objects(args.object_type, args.filter)

no_of_obj = len(data[args.object_type])

msg1 = "Fetched " + str(no_of_obj) + " " + args.object_type + " to apply sharing..."
print(msg1)
dhis.log.info(msg1)

counter = 1
for obj in data[args.object_type]:
    payload = {
        "meta": {
            "allowPublicAccess": True,
            "allowExternalAccess": False
        },
        "object": {
            "id": obj['id'],
            "name": obj['name'],
            "publicAccess": Dhis.public_access[args.publicaccess],
            "externalAccess": False,
            "user": {},
            "userGroupAccesses": [
                {
                    "id": readwrite_usergroup_uid,
                    "access": Dhis.public_access["readwrite"]
                },
                {
                    "id": readonly_usergroup_uid,
                    "access": Dhis.public_access["readonly"]
                }
            ]
        }
    }
    # strip name to match API (e.g. dataElements -> dataElement)
    parameters = {
        'type': args.object_type[:-1],
        'preheatCache': False,
        'id': obj['id']
    }

    # apply sharing
    dhis.share_object(payload, parameters)

    msg2 = "(" + str(counter) + "/" + str(no_of_obj) + ") [OK] " + obj['name']
    print(msg2)
    dhis.log.info(msg2)
    counter += 1
