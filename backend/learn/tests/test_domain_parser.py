from django.test import TestCase
from learn.domain_parser import load_domain_from_file
from learn.models import Domain, Task, ProblemSet


#@pytest.fixture(scope='module')
#def domain():
#    load_domain_from_file('domain/tests/test1.domain.json')
#    domain = Domain.objects.get(name='test1')
#    # TODO: delete the domain (cascade)
#    return domain

class DomainParserTestCase(TestCase):
    # TODO: Use a fixture to avoid parsing the file multiple times, but still
    # having multiple unit tests for better readability.
    def test_load_domain_from_file(self):
        load_domain_from_file('domain/tests/test1.domain.json')
        domain = Domain.objects.get(name='test1')

        # Test entities loaded
        self.assertQuerysetEqual(
            domain.blocks.all(),
            ['<Block: b1>', '<Block: b2>'])
        self.assertQuerysetEqual(
            domain.toolboxes.all(),
            ['<Toolbox: tb1>', '<Toolbox: tb2>'],
            ordered=False)
        self.assertQuerysetEqual(
            domain.tasks.all(),
            ['<Task: t1>', '<Task: t2>', '<Task: t3>'],
            ordered=False)
        self.assertQuerysetEqual(
            domain.problemsets.all(),
            ['<ProblemSet: m1>',
             '<ProblemSet: p1A>', '<ProblemSet: p1B>','<ProblemSet: p1C>',
             '<ProblemSet: m2>',
             '<ProblemSet: p2A>','<ProblemSet: p2B>','<ProblemSet: p2C>'])

        # Test inferred sections
        p2c = ProblemSet.objects.get(name='p2C')
        assert p2c.order == 3
        assert p2c.section == '2.3'
        assert p2c.level == 2

        # Test tasks content
        task = Task.objects.get(pk=1)
        assert task.name == 't1'
        assert task.solution == 'f'
        assert task.setting == {'fields': 'b||kS'}
        # TODO: test task.section


#
#    def test_load_domain_from_file__relationships(self):
#        load_domain_from_file('domain/tests/test1.domain.json')
#        chunk = Chunk.objects.get(name='c1b')
#        self.assertQuerysetEqual(
#            chunk.tasks.all(),
#            ['<Task: t2>', '<Task: t3>'],
#            ordered=False)
#
#    def test_load_domain_params(self):
#        load_domain_from_file('domain/tests/test1.domain.json')
#        domain = Domain.objects.get(name='test1')
#        self.assertQuerysetEqual(
#            domain.params.all(),
#            ['<DomainParam: test1:good_time:t1=10.0>',
#             '<DomainParam: test1:good_time:t2=20.0>',
#             '<DomainParam: test1:good_time:t3=30.0>'],
#            ordered=False)
#
#    def test_load_domain_update_existing_task(self):
#        domain = Domain.objects.create(name='test1')
#        t1 = Task.objects.create(name='t1', setting='{}', solution='')
#        domain.tasks.set([t1])
#        load_domain_from_file('domain/tests/test1.domain.json')
#        t1 = Task.objects.get(name='t1')
#        assert t1.pk == 1
#        assert t1.solution == 'f'
#
#    def test_load_domain_change_task_name(self):
#        domain = Domain.objects.create(name='test1')
#        t0 = Task.objects.create(pk=1, name='t0', setting='{}', solution='')
#        domain.tasks.set([t0])
#        load_domain_from_file('domain/tests/test1.domain.json')
#        self.assertQuerysetEqual(
#            domain.tasks.all(),
#            ['<Task: t1>', '<Task: t2>', '<Task: t3>'],
#            ordered=False)
#        t1 = Task.objects.get(name='t1')
#        assert t1.pk == 1
#        assert not Task.objects.filter(name='t0').exists()
#
    # The following test demonstrates currently not allowed behavior
    # (the test don't pass): it's not possible to rename a task to an existing
    # name, since that could easily lead to data inconsitencies. To load a new
    # domain on local/staging machine, it will be necessary to delete existing
    # data first (make reset_db), because the task IDs were set to match the
    # production DB.
    #def test_load_domain_swap_task_ids(self):
    #    domain = Domain.objects.create(name='test1')
    #    tA = Task.objects.create(pk=2, name='t1', setting='{}', solution='')
    #    tB = Task.objects.create(pk=1, name='t2', setting='{}', solution='')
    #    domain.tasks.set([tA, tB])
    #    load_domain_from_file('domain/tests/test1.domain.json')
    #    assert Task.objects.get(pk=1).name == 't1'
    #    assert Task.objects.get(pk=2).name == 't2'
