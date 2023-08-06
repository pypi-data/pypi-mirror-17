====================
Flis Metadata Client
====================

Client for FLIS applications that require common metadata

Quick start
-----------

#. Add ``flis_metadata.common`` and ``flis_metadata.client``
   to your ``INSTALLED_APPS`` setting like this::

      INSTALLED_APPS = (
          ...
          'flis_metadata.common',
          'flis_metadata.client',
      )

#. Add ``METADATA_REMOTE_HOST`` and ``METADATA_REMOTE_PATH`` into your settings file::

     METADATA_REMOTE_HOST = 'http://localhost:8000'
     METADATA_REMOTE_PATH = ''

#. Run ``python manage.py migrate`` to migrate the common app.

#. Run ``python manage.py sync_remote_models`` to sync the metadata models with
   the remote ones.

How to add a new model
----------------------
We want to move model ``Foo`` from ``flis.someapp`` to be
replicated in all FLIS apps

In this app:
    1. Add the model in ``common/models.py``. Make sure it extends
       ``ReplicatedModel``.

    2. Add ``urls``, ``views`` and ``templates`` to edit it.

    3. Add a fixture having all instances of ``Foo`` for every FLIS app.
      Note:
       This data will be replicated and migrated in every app that uses
       this package, so make sure that the migration includes everything

    4. Update the pip package using ``setup.py``.

In ``flis.someapp`` and other apps using this model
    #. Update ``eaa.flis.metadata`` package in ``requirements.txt`` and
       install it.
    
    #. For every relation to the ``Foo`` model::

           # add a new fake foreign key field
           x = models.ForeingKey(Foo)
           fake_x = models.ForeingKey('common.Foo')

           # or add a new fake many to many field
           y = models.ManyToManyField(Foo)
           fake_y = models.ManyToManyField('common.Foo')

    #. Add a migration to add the new fields

    #. Create a datamigration that
       
       a) Calls ``load_metadata_fixtures`` management command
       b) For every ``x`` copies the same information in ``fake_x`` 
          using the instance found in ``common.Foo``::

                obj.fake_x = orm['common.Foo'].objects.get(title=obj.x.title)

                # or

                for y in obj.y.all():
                  obj.fake_y.add(orm['common.Foo'].objects.get(title=y.title)

    #. Remove the ``Foo`` model and ``x`` fields from
       ``flis.someapp``.

    #. Create an automatic schemamigration to reflect the removals.

    #. Rename ``fake_x`` fields to ``x`` in ``models.py``.

    #. In the migration generated at step 5 rename the fields and M2M tables from
       ``fake_x`` to ``x``.

    #. Run the migration in different corner cases.
     Note:
      You can browse through ``flis.flip``, ``flis.horizon-scanning-tool`` or
      ``flis.live_catalogue`` to see an example of such migrations.
