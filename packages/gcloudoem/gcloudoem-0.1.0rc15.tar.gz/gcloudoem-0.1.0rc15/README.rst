Google Datastore Object-Entity-Mapper
=====================================
Python object to entity mapper for Google Datastore with Django support.

Quickstart
----------
::

    from gcloudoem import *

    class TestEntity(Entity):
        name = TextProperty()


    class OtherTestEntity(Entity):
        address = TextProperty(default='blah')
        te = ListProperty(ReferenceProperty(TestEntity))

    connect(dataset_id='dataset_id', namespace='demo')

    es = TestEntity.objects.filter(name='Alice')
    oe = OtherTestEntity(te=[e for e in es])
    oe.save()
    ot = OtherTestEntity.objects.get(pk=oe.key.name_or_id)
    print(ot.key.name_or_id, [te.name for te in ot.te])
    query = query.Query(TestEntity)
    query.add_filter("name", "=", "Kris")
    cursor = query()
    print([(e.name, e.key.name_or_id,) for e in list(o)])

Copyright and License
---------------------

Gcloudoem is Copyright (C) the respective authors of the files, as noted at the top of each file. If not noted, it is
Copyright 2015 Kapiche Ltd.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with 
the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an 
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the License for the 
specific language governing permissions and limitations under the License.
