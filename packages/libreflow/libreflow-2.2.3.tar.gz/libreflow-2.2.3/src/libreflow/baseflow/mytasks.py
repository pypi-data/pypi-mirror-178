import time
import pprint
import collections
from kabaret import flow
from .users import PresetSessionValue


class TaskItem(flow.Object):

    _action            = flow.Parent(3)

    task_id            = flow.SessionParam()
    task_type          = flow.SessionParam()
    task_status        = flow.SessionParam()
    task_oid           = flow.SessionParam()
    entity_type        = flow.SessionParam() # Asset or Shot
    entity_type_name   = flow.SessionParam() # Asset Type or Sequence name
    entity_name        = flow.SessionParam() # Asset or Shot name
    entity_description = flow.SessionParam()
    shot_frames        = flow.SessionParam()
    dft_task_name      = flow.SessionParam()
    primary_files      = flow.SessionParam(list)

    def set_shot_duration(self):
        data = self._action.kitsu.get_shot_data(self.entity_name.get(), self.entity_type_name.get())
        return self.shot_frames.set(data['nb_frames'])

    def find_default_task(self):
        dft_tasks = self.root().project().get_task_manager().default_tasks.mapped_items()
        for task in dft_tasks:
            if self.task_type.get() in task.kitsu_tasks.get():
                self.dft_task_name.set(task.name())

    def set_task_oid(self):
        if self.entity_type.get() == 'Shot':
            film = self.root().project().films.mapped_items()[0]
            if film.sequences.has_mapped_name(self.entity_type_name.get()):
                sequence = film.sequences[self.entity_type_name.get()]
                if sequence.shots.has_mapped_name(self.entity_name.get()):
                    shot = sequence.shots[self.entity_name.get()]
                    if shot.tasks.has_mapped_name(self.dft_task_name.get()):
                        task = shot.tasks[self.dft_task_name.get()]
                        self.task_oid.set(task.oid())
                        self.primary_files.set(task.get_primary_files())
                    else:
                        self.task_oid.set(shot.oid())
        else:
            asset_types = self.root().project().asset_types
            if asset_types.has_mapped_name(self.entity_type_name.get()):
                asset_type = asset_types[self.entity_type_name.get()]
                if asset_type.assets.has_mapped_name(self.entity_name.get()):
                    asset = asset_type.assets[self.entity_name.get()]
                    if asset.tasks.has_mapped_name(self.dft_task_name.get()):
                        task = asset.tasks[self.dft_task_name.get()]
                        self.task_oid.set(task.oid())
                        self.primary_files.set(task.get_primary_files())
                    else:
                        self.task_oid.set(asset.oid())


class MyTasksMap(flow.DynamicMap):

    _settings = flow.Parent()
    _action = flow.Parent(2)

    def __init__(self, parent, name):
        super(MyTasksMap, self).__init__(parent, name)
        self._cache = None
        self._cache_ttl = self._settings.cache_ttl.get()
        self._cache_birth = -1
        self._cache_key = None

    @classmethod
    def mapped_type(cls):
        return TaskItem

    def columns(self):
        return ['Task', 'Status', 'Type', 'Type Name', 'Name']

    def mapped_names(self, page_num=0, page_size=None):
        cache_key = (page_num, page_size)
        if (
            self._cache is None
            or time.time() - self._cache_birth > self._cache_ttl
            or self._cache_key != cache_key
        ):
            self._mng.children.clear()
            tasks = self._action.kitsu.get_assign_tasks()
            if 'DONE' in self._settings.task_statues_filter.get():
                tasks += self._action.kitsu.get_done_tasks()

            self._cache = {}

            for i, item in enumerate(tasks):
                data = {}
                # Filter
                if item['task_status_short_name'].upper() not in self._settings.task_statues_filter.get():
                    continue
                if 'task_type_for_entity' in item:
                    if item['task_type_for_entity'] == "Asset":
                        if item['entity_type_name'] == 'x':
                            continue
                        if item['task_type_name'] == 'FDT':
                            continue

                        data.update(dict(
                            task_id=item['id'], 
                            task_type=item['task_type_name'],
                            task_status=item['task_status_short_name'].upper(),
                            entity_type=item['task_type_for_entity'],
                            entity_type_name=item['entity_type_name'],
                            entity_name=item['entity_name'],
                            entity_description=item['entity_description'],
                            updated_date=item['updated_at']
                        ))
                    else:
                        data.update(dict(
                            task_id=item['id'], 
                            task_type=item['task_type_name'],
                            task_status=item['task_status_short_name'].upper(),
                            entity_type=item['entity_type_name'],
                            entity_type_name=item['sequence_name'],
                            entity_name=item['entity_name'],
                            entity_description=item['entity_description'],
                            updated_date=item['updated_at']
                        ))
                else:
                    data.update(dict(
                        task_id=item['id'], 
                        task_type=item['task_type_name'],
                        task_status=item['task_status_short_name'].upper(),
                        entity_type=item['entity_type_name'],
                        entity_type_name=item['sequence_name'],
                        entity_name=item['entity_name'],
                        entity_description=item['entity_description'],
                        updated_date=item['updated_at']
                    ))
                self._cache['task'+str(i)] = data

            # Sorting
            if self._settings.task_sorted.get() == 'Entity name':
                self._cache = collections.OrderedDict(sorted(
                    self._cache.items(),
                    key=lambda data: (data[1]['entity_type_name'], data[1]['entity_name']
                )))
            elif self._settings.task_sorted.get() == 'Status':
                self._cache = collections.OrderedDict(sorted(
                    self._cache.items(),
                    key=lambda data: data[1]['task_status']
                ))
            elif self._settings.task_sorted.get() == 'Latest update':
                self._cache = collections.OrderedDict(sorted(
                    self._cache.items(),
                    key=lambda data: data[1]['updated_date'],
                    reverse=True
                ))
           
            self._cache_key = cache_key
            self._cache_birth = time.time()

        return self._cache.keys()
    
    def touch(self):
        self._cache = None
        super(MyTasksMap, self).touch()

    def _configure_child(self, child):
        child.task_id.set(self._cache[child.name()]['task_id'])
        child.task_type.set(self._cache[child.name()]['task_type'])
        child.task_status.set(self._cache[child.name()]['task_status'])
        child.entity_type.set(self._cache[child.name()]['entity_type'])
        child.entity_type_name.set(self._cache[child.name()]['entity_type_name'])
        child.entity_name.set(self._cache[child.name()]['entity_name'])
        child.entity_description.set(self._cache[child.name()]['entity_description'])

        if self._cache[child.name()]['entity_type'] == 'Shot':
            child.set_shot_duration()
        child.find_default_task()
        child.set_task_oid()

    def _fill_row_cells(self, row, item):
        row["Task"] = item.task_type.get()
        row["Status"] = item.task_status.get()
        row["Type"] = item.entity_type.get()
        row["Type Name"] = item.entity_type_name.get()
        row["Name"] = item.entity_name.get()


class MyTasksSettings(flow.Object):

    tasks               = flow.Child(MyTasksMap)
    task_statues_filter = flow.SessionParam([], PresetSessionValue)
    task_sorted         = flow.SessionParam(None, PresetSessionValue)
    cache_ttl           = flow.Param(120)

    def check_default_values(self):
        self.task_statues_filter.apply_preset()
        self.task_sorted.apply_preset()

    def update_presets(self):
        self.task_statues_filter.update_preset()
        self.task_sorted.update_preset()


class MyTasks(flow.Object):

    settings = flow.Child(MyTasksSettings)

    def __init__(self, parent, name):
        super(MyTasks, self).__init__(parent, name)
        self.kitsu = self.root().project().admin.kitsu.gazu_api
        self.settings.check_default_values()

    def get_tasks(self, force_update=False):
        if force_update:
            self.settings.tasks.touch()
        return self.settings.tasks.mapped_items()

    def get_task_statutes(self):
        return self.kitsu.get_task_statutes(short_name=True)

    def get_task_comments(self, task_id):
        return self.kitsu.get_all_comments_for_task(task_id)

    def get_server_url(self):
        return self.kitsu.get_server_url()
    
    def get_project_id(self):
        return self.kitsu.get_project_id()

    def get_project_oid(self):
        return self.root().project().oid()

    def _fill_ui(self, ui):
        ui["custom_page"] = "libreflow.baseflow.ui.mytasks.MyTasksPageWidget"
