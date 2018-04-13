from datetime import date
from django.test import TestCase
from django.utils import timezone
from learn.models import Block, Task, Chunk, ProblemSet, Student, Skill, TaskSession
from learn.models import ProgramSnapshot, Domain, DomainParam
from learn.utils.time import ms


class BlockTestCase(TestCase):
    def test_blocks_exists(self):
        assert Block.objects.exists()

    def test_blocks_are_ordered(self):
        first_retrieved_blocks = list(Block.objects.all())[:3]
        first_expected_blocks = [
            Block.objects.get(name='fly'),
            Block.objects.get(name='shoot'),
            Block.objects.get(name='repeat')]
        assert first_retrieved_blocks == first_expected_blocks

    def test_str_returns_name(self):
        carrot_block = Block(name='carrot', order=4)
        assert str(carrot_block) == 'carrot'


class ChunkTestCase(TestCase):
    def test_chunks_order_by_section(self):
        chunk1 = Chunk.objects.create(name='c1', section='1.2')
        chunk2 = Chunk.objects.create(name='c2', section='1.1')
        assert list(Chunk.objects.all()) == [chunk2, chunk1]

    def test_chunks_order_by_type_first(self):
        chunk1 = Chunk.objects.create(type='b', name='c1', section='1.1')
        chunk2 = Chunk.objects.create(type='a', name='c2', section='1.2')
        assert list(Chunk.objects.all()) == [chunk2, chunk1]

    def test_str(self):
        chunk = Chunk.objects.create(
            section='2.3', type='concept', name='loops')
        assert str(chunk) == 'concept:loops'

    def test_level(self):
        chunk = Chunk.objects.create(section='3.1.5')
        assert chunk.level == 3

    def test_order(self):
        chunk = Chunk.objects.create(section='3.1.5')
        assert chunk.order == 5

    def test_content_setting(self):
        chunk = Chunk.objects.create(content={'setting': 4})
        assert chunk.setting == 4

    def test_default_setting(self):
        chunk = Chunk.objects.create()
        assert chunk.setting == {}


class ProblemSetTestCase(TestCase):
    def test_default_granularity(self):
        ps = ProblemSet.objects.create()
        assert ps.granularity == 'phase'

    def test_type(self):
        ps = ProblemSet.objects.create()
        assert ps.type == 'ps.phase'

    def test_mission(self):
        ps = ProblemSet.objects.create(granularity='mission')
        assert ps.type == 'ps.mission'

    def test_str(self):
        ps = ProblemSet.objects.create(
            section='2.3', granularity='mission', name='loops')
        assert str(ps) == 'loops'
        assert repr(ps) == '<ProblemSet: loops>'

    def test_is_mission(self):
        mission = ProblemSet.objects.create(granularity='mission')
        phase = ProblemSet.objects.create(granularity='phase')
        assert mission.is_mission
        assert not phase.is_mission

    def test_parts(self):
        mission = ProblemSet.objects.create(granularity='mission')
        phase1 = ProblemSet.objects.create(name='p1', parent=mission)
        phase2 = ProblemSet.objects.create(name='p2', parent=mission)
        self.assertQuerysetEqual(
            mission.parts.all(), ['<ProblemSet: p1>', '<ProblemSet: p2>'])

    def test_phases(self):
        mission = ProblemSet.objects.create(granularity='mission')
        phase1 = ProblemSet.objects.create(parent=mission)
        phase2 = ProblemSet.objects.create(parent=mission)
        assert mission.phases == [phase1, phase2]

    def test_phases_set_from_mission(self):
        phase1 = ProblemSet.objects.create()
        phase2 = ProblemSet.objects.create()
        mission = ProblemSet.objects.create(granularity='mission')
        mission.parts.set([phase1, phase2])
        assert mission.phases == [phase1, phase2]

    def test_n_tasks(self):
        ps = ProblemSet.objects.create()
        Task.objects.create(problemset=ps)
        Task.objects.create(problemset=ps)
        Task.objects.create(problemset=ps)
        assert ps.n_tasks == 3

    def test_n_parts(self):
        ps = ProblemSet.objects.create()
        ProblemSet.objects.create(parent=ps)
        ProblemSet.objects.create(parent=ps)
        assert ps.n_parts == 2

    def test_add_part(self):
        ps = ProblemSet.objects.create(section='7.3')
        ps.add_part(name='p1')
        ps.add_part(name='p2')
        part = ps.parts.last()
        assert part.name == 'p2'
        assert part.parent == ps
        assert part.granularity == 'phase'
        assert part.section == '7.3.2'

    def test_add_task(self):
        ps = ProblemSet.objects.create(section='7.3')
        ps.add_task(name='t1')
        ps.add_task(name='t2')
        task = ps.tasks.last()
        assert task.name == 't2'
        assert task.problemset == ps
        assert task.section == '7.3.2'


class TaskTestCase(TestCase):
    def test_type(self):
        task = Task.objects.create()
        assert task.type == 'task'

    def test_str(self):
        task = Task.objects.create(name='carrot', section='2.3')
        assert str(task) == 'carrot'

    def test_mission(self):
        mission = ProblemSet.objects.create(granularity='mission')
        phase = ProblemSet.objects.create(parent=mission)
        task = Task.objects.create(problemset=phase)
        assert task.mission == mission


class StudentTestCase(TestCase):
    def test_get_skill__existing(self):
        chunk = Chunk.objects.create(name='c1')
        student = Student.objects.create()
        Skill.objects.create(student=student, chunk=chunk, value=0.25)
        assert student.get_skill(chunk) == 0.25

    def test_get_skill__nonexisting(self):
        chunk = Chunk.objects.create(name='c1')
        student = Student.objects.create()
        assert student.get_skill(chunk) == 0

    def test_str(self):
        student = Student.objects.create(id=10)
        assert str(student) == 's10'


class TaskSessionTestCase(TestCase):
    def test_date(self):
        task = Task.objects.create()
        student = Student.objects.create()
        ts = TaskSession.objects.create(
            student=student, task=task,
            start=timezone.datetime(2017, 1, 1, 8, 0, 0, tzinfo=timezone.utc),
            end=timezone.datetime(2017, 1, 1, 8, 2, 0, tzinfo=timezone.utc))
        assert ts.date == date(2017, 1, 1)

    def test_time_spent(self):
        task = Task.objects.create()
        student = Student.objects.create()
        ts = TaskSession.objects.create(
            student=student, task=task,
            start=timezone.datetime(2017, 1, 1, 8, 0, 0, tzinfo=timezone.utc),
            end=timezone.datetime(2017, 1, 1, 8, 2, 5, tzinfo=timezone.utc))
        assert ts.time_spent == 125

    def test_str(self):
        task = Task.objects.create(name='carrot')
        student = Student.objects.create(id=10)
        ts = TaskSession.objects.create(id=11, student=student, task=task)
        assert str(ts) == '[11] s10-carrot'

    def test_performance_is_ordered(self):
        assert TaskSession.UNSOLVED < TaskSession.POOR
        assert TaskSession.POOR < TaskSession.GOOD
        assert TaskSession.GOOD < TaskSession.EXCELLENT


class ProgramSnapshotTestCase(TestCase):
    def test_str(self):
        snapshot = ProgramSnapshot(id=5, program='ffr')
        assert str(snapshot) == '[5] ffr'

    def test_order_first(self):
        ts = _create_task_session()
        snapshot = ProgramSnapshot.objects.create(task_session=ts)
        assert snapshot.order == 1

    def test_order_first_for_given_granularity(self):
        ts = _create_task_session()
        edit_snapshot = ProgramSnapshot.objects.create(
            task_session=ts, granularity=ProgramSnapshot.EDIT)
        execution_snapshot = ProgramSnapshot.objects.create(
            task_session=ts, granularity=ProgramSnapshot.EXECUTION)
        assert edit_snapshot.order == 1
        assert execution_snapshot.order == 1

    def test_order_by_time(self):
        ts = _create_task_session()
        snapshot1 = ProgramSnapshot.objects.create(
            task_session=ts,
            time=timezone.datetime(2017, 1, 1, 8, 0, 0, tzinfo=timezone.utc))
        snapshot2 = ProgramSnapshot.objects.create(
            task_session=ts,
            time=timezone.datetime(2017, 1, 1, 8, 0, 10, tzinfo=timezone.utc))
        assert snapshot1.order == 1
        assert snapshot2.order == 2

    def test_order_by_time_within_granularity(self):
        ts = _create_task_session()
        edit_snapshot1 = ProgramSnapshot.objects.create(
            task_session=ts,
            time=timezone.datetime(2017, 1, 1, 8, 0, 0, tzinfo=timezone.utc),
            granularity=ProgramSnapshot.EDIT)
        execution_snapshot1 = ProgramSnapshot.objects.create(
            task_session=ts,
            time=timezone.datetime(2017, 1, 1, 8, 0, 10, tzinfo=timezone.utc),
            granularity=ProgramSnapshot.EXECUTION)
        edit_snapshot2 = ProgramSnapshot.objects.create(
            task_session=ts,
            time=timezone.datetime(2017, 1, 1, 8, 0, 20, tzinfo=timezone.utc),
            granularity=ProgramSnapshot.EDIT)
        assert edit_snapshot1.order == 1
        assert execution_snapshot1.order == 1
        assert edit_snapshot2.order == 2

    def test_time_from_start(self):
        ts = _create_task_session_at(ms('0:00'))
        snapshot = ProgramSnapshot.objects.create(task_session=ts, time=ms('0:10'))
        assert snapshot.time_from_start == 10

    def test_time_from_start_over_minute(self):
        ts = _create_task_session_at(ms('0:00'))
        snapshot = ProgramSnapshot.objects.create(task_session=ts, time=ms('2:05'))
        assert snapshot.time_from_start == 125


class SkillTestCase(TestCase):
    def test_str(self):
        student = Student.objects.create(pk=10)
        chunk = Chunk.objects.create(name='carrot')
        skill = Skill(student=student, chunk=chunk, value=0.8)
        assert str(skill) == 's10:carrot=0.8'


class DomainParamTestCase(TestCase):
    def test_str(self):
        domain = Domain.objects.create(name='d')
        chunk = Chunk.objects.create(name='c')
        param = DomainParam(domain=domain, chunk=chunk, name='n', value=3)
        assert str(param) == 'd:n:c=3'


def _create_task_session():
    task = Task.objects.create(name='carrot')
    student = Student.objects.create()
    ts = TaskSession.objects.create(student=student, task=task)
    return ts


def _create_task_session_at(time):
    task = Task.objects.create(name='carrot')
    student = Student.objects.create()
    ts = TaskSession.objects.create(student=student, task=task, start=time)
    return ts
