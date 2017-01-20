"""initial schema

Revision ID: 5800d2420705
Revises: 
Create Date: 2017-01-19 20:54:03.697751

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5800d2420705'
down_revision = None
branch_labels = None
depends_on = None

exercise_table = sa.table('exercises',
                          sa.column('id', sa.Integer),
                          sa.column('qb_id', sa.String),
                          sa.column('topic', sa.String),
                          sa.column('data', sa.JSON),
                          sa.column('level', sa.Integer)
                          )


def upgrade():
    op.create_table('exercises',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('qb_id', sa.String(), nullable=True),
    sa.Column('topic', sa.String(), nullable=False),
    sa.Column('data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('qb_id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=120), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
    sa.Column('last_login_at', sa.DateTime(), nullable=True),
    sa.Column('current_login_at', sa.DateTime(), nullable=True),
    sa.Column('last_login_ip', sa.String(length=100), nullable=True),
    sa.Column('current_login_ip', sa.String(length=100), nullable=True),
    sa.Column('login_count', sa.Integer(), nullable=True),
    sa.Column('registered_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('roles_users',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_table('user_subjects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('external_id', sa.String(length=128), nullable=True),
    sa.Column('mturk_worker_id', sa.String(length=128), nullable=False),
    sa.Column('status', sa.String(length=128), nullable=True),
    sa.Column('experiment_group', sa.String(length=128), nullable=True),
    sa.Column('data_string', sa.Text(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subject_assignments',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('subject_id', sa.Integer(), nullable=False),
                    sa.Column('mturk_assignment_id', sa.String(length=128), nullable=False),
                    sa.Column('mturk_hit_id', sa.String(length=128),
                              nullable=False),
                    sa.Column('assignment_phase', sa.String(length=50), nullable=True),
                    sa.Column('ua_raw', sa.String(length=255), nullable=True),
                    sa.Column('ua_browser', sa.String(length=128), nullable=True),
                    sa.Column('ua_browser_version', sa.String(length=128), nullable=True),
                    sa.Column('ua_os', sa.String(length=128), nullable=True),
                    sa.Column('ua_os_version', sa.String(length=128), nullable=True),
                    sa.Column('ua_device', sa.String(length=128), nullable=True),
                    sa.Column('skill_level', sa.String(length=50), nullable=True),
                    sa.Column('education', sa.String(length=50), nullable=True),
                    sa.Column('gender', sa.String(length=50), nullable=True),
                    sa.Column('english_level', sa.String(length=50), nullable=True),
                    sa.Column('comments', sa.Text(), nullable=True),
                    sa.Column('did_cheat', sa.Boolean(), nullable=True),
                    sa.Column('did_timeout', sa.Boolean(), nullable=False),
                    sa.Column('did_quit', sa.Boolean(), nullable=False),
                    sa.Column('is_complete', sa.Boolean(), nullable=False),
                    sa.Column('mturk_completion_code', sa.String(length=255), nullable=True),
                    sa.Column('mturk_assignment_status', sa.String(length=100), nullable=True),
                    sa.Column('mturk_assignment_status_date', sa.DateTime(), nullable=True),
                    sa.Column('assignment_results', postgresql.JSON(astext_type=sa.Text()), nullable=True),
                    sa.Column('assignment_predictions', postgresql.JSON(astext_type=sa.Text()), nullable=True),
                    sa.Column('created_on', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['subject_id'], ['user_subjects.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('assignment_responses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('assignment_id', sa.Integer(), nullable=True),
    sa.Column('exercise_id', sa.Integer(), nullable=True),
    sa.Column('selection', sa.Integer(), nullable=False),
    sa.Column('credit', sa.Float(), nullable=False),
    sa.Column('user_response_time', sa.Float(), nullable=False),
    sa.Column('started_on', sa.DateTime(), nullable=False),
    sa.Column('completed_on', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['assignment_id'], ['subject_assignments.id'], ),
    sa.ForeignKeyConstraint(['exercise_id'], ['exercises.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('assignment_sessions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('assignment_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=100), nullable=True),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['assignment_id'], ['subject_assignments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    op.bulk_insert(exercise_table,
                   [
                       {'topic': 'Expressions', 'qb_id': '14296v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '1.0', 'markup': '0',
                                'html': '<p>0</p>'},
                               {'credit': '0.0', 'markup': '1',
                                'html': '<p>1</p>'}], 'content': {
                               'markup': 'Evaluate the Boolean expression:\r\n\r\n$(1+0)\\cdot(0\\cdot(1+1))$',
                               'html': '<p>Evaluate the Boolean expression:</p>\n<p>$(1+0)\\cdot(0\\cdot(1+1))$</p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Andrew Waters',
                                                                               'id': 165}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Andrew Waters',
                                                                       'id': 165}]},
                                               'url': 'http://quadbase.org/questions/q14296v1',
                                               'answer_can_be_sketched': None,
                                               'id': 'q14296v1'}}, 'level': 2,
                        'id': 11},
                       {'topic': 'Terminology', 'qb_id': '14462v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '1.0', 'markup': 'AND',
                                'html': '<p>AND</p>'},
                               {'credit': '0.0', 'markup': 'OR',
                                'html': '<p>OR</p>'},
                               {'credit': '0.0', 'markup': 'NOT',
                                'html': '<p>NOT</p>'},
                               {'credit': '0.0', 'markup': 'NAND',
                                'html': '<p>NAND</p>'},
                               {'credit': '0.0', 'markup': 'NOR',
                                'html': '<p>NOR</p>'},
                               {'credit': '0.0', 'markup': 'XOR',
                                'html': '<p>XOR</p>'},
                               {'credit': '0.0', 'markup': 'XNOR',
                                'html': '<p>XNOR</p>'}], 'content': {
                               'markup': 'This is the electronic symbol for which logic gate?\r\n\r\n{img:1.png}',
                               'html': '<p>This is the electronic symbol for which logic gate?</p>\n<p><center><img src="https://quadbase.org/system/attachments/2615/medium/7ebde8baf3ad3b8a537d52ea41946827.png"></center></p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Phillip  Grimaldi',
                                                                               'id': 294}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Phillip  Grimaldi',
                                                                       'id': 294}]},
                                               'url': 'http://quadbase.org/questions/q14462v1',
                                               'answer_can_be_sketched': False,
                                               'id': 'q14462v1'}}, 'level': 0,
                        'id': 16},
                       {'topic': 'TT', 'qb_id': '14317v2', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0', 'markup': 'XY',
                                'html': '<p>XY</p>'},
                               {'credit': '1.0', 'markup': "X'Y'+X'Y+XY'",
                                'html': "<p>X'Y'+X'Y+XY'</p>"},
                               {'credit': '0.0', 'markup': "X+Y'",
                                'html': "<p>X+Y'</p>"},
                               {'credit': '0.0', 'markup': "X'Y'+X'Y+XY'+XY",
                                'html': "<p>X'Y'+X'Y+XY'+XY</p>"},
                               {'credit': '0.0', 'markup': "X'Y'",
                                'html': "<p>X'Y'</p>"}], 'content': {
                               'markup': 'Consider the truth table below. \r\n\r\n{img:4.1.PNG}\r\n\r\nThe function Z takes as input X and Y. Write a sum-of-products Boolean expression for Z.\r\n\r\n\r\n',
                               'html': '<p>Consider the truth table below. </p>\n<p><center><img src="https://quadbase.org/system/attachments/2484/medium/cac796037d7415d4c98b06d226090394.png"></center></p>\n<p>The function Z takes as input X and Y. Write a sum-of-products Boolean expression for Z.</p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Andrew Waters',
                                                                               'id': 165}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Andrew Waters',
                                                                       'id': 165}]},
                                               'url': 'http://quadbase.org/questions/q14317v2',
                                               'answer_can_be_sketched': False,
                                               'id': 'q14317v2'}}, 'level': 2,
                        'id': 17},
                       {'topic': 'Terminology', 'qb_id': '14454v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '1.0', 'markup': 'A AND B',
                                'html': '<p>A AND B</p>'},
                               {'credit': '0.0', 'markup': 'A OR B',
                                'html': '<p>A OR B</p>'},
                               {'credit': '0.0', 'markup': 'A NAND B',
                                'html': '<p>A NAND B</p>'},
                               {'credit': '0.0', 'markup': 'A NOR B',
                                'html': '<p>A NOR B</p>'},
                               {'credit': '0.0', 'markup': 'A XOR B',
                                'html': '<p>A XOR B</p>'},
                               {'credit': '0.0', 'markup': 'A XNOR B',
                                'html': '<p>A XNOR B</p>'}], 'content': {
                               'markup': 'A • B = ?',
                               'html': '<p>A • B = ?</p>'}, 'attribution': {
                               'license': {
                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                               'authors': [
                                   {'name': 'Phillip  Grimaldi', 'id': 294}],
                               'copyright_holders': [
                                   {'name': 'Phillip  Grimaldi', 'id': 294}]},
                                               'url': 'http://quadbase.org/questions/q14454v1',
                                               'answer_can_be_sketched': False,
                                               'id': 'q14454v1'}}, 'level': 0,
                        'id': 18},
                       {'topic': 'TT', 'qb_id': '14301v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0',
                                'markup': '0, 0, 1, 1, 0, 0, 1, 1',
                                'html': '<p>0, 0, 1, 1, 0, 0, 1, 1</p>'},
                               {'credit': '0.0',
                                'markup': '1, 1, 0, 0, 1, 0, 0, 1',
                                'html': '<p>1, 1, 0, 0, 1, 0, 0, 1</p>'},
                               {'credit': '1.0',
                                'markup': '0, 0, 1, 1, 1, 0, 1, 0',
                                'html': '<p>0, 0, 1, 1, 1, 0, 1, 0</p>'},
                               {'credit': '0.0',
                                'markup': '0, 0, 1, 0, 1, 1, 0, 1',
                                'html': '<p>0, 0, 1, 0, 1, 1, 0, 1</p>'},
                               {'credit': '0.0',
                                'markup': '0, 1, 1, 1, 0, 1, 0, 0',
                                'html': '<p>0, 1, 1, 1, 0, 1, 0, 0</p>'}],
                                               'content': {
                                                   'markup': "Let g = ABC'+AB'C'+A'BC'+A'BC.\r\n\r\nFill in the truth table below. g for A = B = C = 0 is the first number in each answer choice; g for A = B = C = 1 is the last number.\r\n\r\n{img:truth table.PNG}",
                                                   'html': '<p>Let g = ABC\'+AB\'C\'+A\'BC\'+A\'BC.</p>\n<p>Fill in the truth table below. g for A = B = C = 0 is the first number in each answer choice; g for A = B = C = 1 is the last number.</p>\n<p><center><img src="https://quadbase.org/system/attachments/2483/medium/97f80eac7d93300bb5cd08f737b30931.png"></center></p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Andrew Waters',
                                                                               'id': 165}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Andrew Waters',
                                                                       'id': 165}]},
                                               'url': 'http://quadbase.org/questions/q14301v1',
                                               'answer_can_be_sketched': None,
                                               'id': 'q14301v1'}}, 'level': 3,
                        'id': 19},
                       {'topic': 'Circuits', 'qb_id': '14274v2', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0', 'markup': '0',
                                'html': '<p>0</p>'},
                               {'credit': '0.0', 'markup': '1',
                                'html': '<p>1</p>'},
                               {'credit': '0.0', 'markup': '$X$',
                                'html': '<p>$X$</p>'},
                               {'credit': '1.0', 'markup': '$Y$',
                                'html': '<p>$Y$</p>'}], 'content': {
                               'markup': '{img:mux_circuit_1.png}\r\n\r\nConsider this digital circuit. What will it output if S=1?\r\n\r\n',
                               'html': '<p><center><img src="https://quadbase.org/system/attachments/2592/medium/8277e65494306811e1e6765b77275c73.png"></center></p>\n<p>Consider this digital circuit. What will it output if S=1?</p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Andrew Waters',
                                                                               'id': 165}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Andrew Waters',
                                                                       'id': 165}]},
                                               'url': 'http://quadbase.org/questions/q14274v2',
                                               'answer_can_be_sketched': False,
                                               'id': 'q14274v2'}}, 'level': 3,
                        'id': 21},
                       {'topic': 'TT', 'qb_id': '14447v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0', 'markup': 'Logic Gates',
                                'html': '<p>Logic Gates</p>'},
                               {'credit': '1.0', 'markup': 'Truth tables',
                                'html': '<p>Truth tables</p>'},
                               {'credit': '0.0', 'markup': 'Digital circuits',
                                'html': '<p>Digital circuits</p>'},
                               {'credit': '0.0', 'markup': 'None of the above',
                                'html': '<p>None of the above</p>'}],
                                               'content': {
                                                   'markup': 'Select the answer that best completes the following sentence. \r\n\r\n$\\_\\_\\_\\_\\_\\_\\_\\_$ show the output of a boolean expression for every possible combination of inputs. ',
                                                   'html': '<p>Select the answer that best completes the following sentence. </p>\n<p>$\\_\\_\\_\\_\\_\\_\\_\\_$ show the output of a boolean expression for every possible combination of inputs.</p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Phillip  Grimaldi',
                                                                               'id': 294}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Phillip  Grimaldi',
                                                                       'id': 294}]},
                                               'url': 'http://quadbase.org/questions/q14447v1',
                                               'answer_can_be_sketched': False,
                                               'id': 'q14447v1'}}, 'level': 1,
                        'id': 22},
                       {'topic': 'Circuits', 'qb_id': '14310v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0', 'markup': 'NOR',
                                'html': '<p>NOR</p>'},
                               {'credit': '0.0', 'markup': 'AND',
                                'html': '<p>AND</p>'},
                               {'credit': '1.0', 'markup': 'OR',
                                'html': '<p>OR</p>'},
                               {'credit': '0.0', 'markup': 'NAND',
                                'html': '<p>NAND</p>'},
                               {'credit': '0.0', 'markup': 'XOR',
                                'html': '<p>XOR</p>'}], 'content': {
                               'markup': "Below is a partially completed circuit for M=A'B+C. It is missing a logic gate in the box. Which logic gate correctly completes the circuit?\r\n\r\n{img:Selection_005.png}",
                               'html': '<p>Below is a partially completed circuit for M=A\'B+C. It is missing a logic gate in the box. Which logic gate correctly completes the circuit?</p>\n<p><center><img src="https://quadbase.org/system/attachments/2517/medium/cb59799a456276a0933ac94682cb5eed.png"></center></p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Andrew Waters',
                                                                               'id': 165}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Andrew Waters',
                                                                       'id': 165}]},
                                               'url': 'http://quadbase.org/questions/q14310v1',
                                               'answer_can_be_sketched': None,
                                               'id': 'q14310v1'}}, 'level': 1,
                        'id': 25},
                       {'topic': 'TT', 'qb_id': '14305v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0', 'markup': '1, 0, 1, 1',
                                'html': '<p>1, 0, 1, 1</p>'},
                               {'credit': '0.0', 'markup': '1, 0, 0, 0',
                                'html': '<p>1, 0, 0, 0</p>'},
                               {'credit': '1.0', 'markup': '0, 0, 1, 0',
                                'html': '<p>0, 0, 1, 0</p>'},
                               {'credit': '0.0', 'markup': '1, 1, 1, 1',
                                'html': '<p>1, 1, 1, 1</p>'},
                               {'credit': '0.0', 'markup': '0, 0, 0, 0',
                                'html': '<p>0, 0, 0, 0</p>'}], 'content': {
                               'markup': 'Jillian and Jackson go swimming when the weather is hot and there is no rain. They decide to make a circuit, with inputs H (hot) and R (rain). It outputs S (swimming). Fill in the truth table below for the circuit.\r\n\r\n{img:Selection_001.png}\r\n\r\nS for H = R = 0 is the first number in each answer choice; S for H = R = 1 is the last number.',
                               'html': '<p>Jillian and Jackson go swimming when the weather is hot and there is no rain. They decide to make a circuit, with inputs H (hot) and R (rain). It outputs S (swimming). Fill in the truth table below for the circuit.</p>\n<p><center><img src="https://quadbase.org/system/attachments/2507/medium/372f5ec5f6eea9b471e4c0adfa25d164.png"></center></p>\n<p>S for H = R = 0 is the first number in each answer choice; S for H = R = 1 is the last number.</p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Andrew Waters',
                                                                               'id': 165}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Andrew Waters',
                                                                       'id': 165}]},
                                               'url': 'http://quadbase.org/questions/q14305v1',
                                               'answer_can_be_sketched': None,
                                               'id': 'q14305v1'}}, 'level': 2,
                        'id': 31},
                       {'topic': 'Terminology', 'qb_id': '14313v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0',
                                'markup': 'Truth tables are often the first thing a circuit designer knows about a circuit.',
                                'html': '<p>Truth tables are often the first thing a circuit designer knows about a circuit.</p>'},
                               {'credit': '0.0',
                                'markup': 'Circuits are designed directly from Boolean expressions.',
                                'html': '<p>Circuits are designed directly from Boolean expressions.</p>'},
                               {'credit': '1.0', 'markup': 'A and B.',
                                'html': '<p>A and B.</p>'}], 'content': {
                               'markup': 'Why is it important to derive Boolean expressions from truth tables?',
                               'html': '<p>Why is it important to derive Boolean expressions from truth tables?</p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Andrew Waters',
                                                                               'id': 165}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Andrew Waters',
                                                                       'id': 165}]},
                                               'url': 'http://quadbase.org/questions/q14313v1',
                                               'answer_can_be_sketched': None,
                                               'id': 'q14313v1'}}, 'level': 1,
                        'id': 32},
                       {'topic': 'TT', 'qb_id': '14306v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '1.0', 'markup': "S = HR'",
                                'html': "<p>S = HR'</p>"},
                               {'credit': '0.0', 'markup': "S = H'R",
                                'html': "<p>S = H'R</p>"},
                               {'credit': '0.0', 'markup': "S = (HR)'",
                                'html': "<p>S = (HR)'</p>"},
                               {'credit': '0.0', 'markup': "S = H'R'",
                                'html': "<p>S = H'R'</p>"},
                               {'credit': '0.0', 'markup': 'S = H',
                                'html': '<p>S = H</p>'}], 'content': {
                               'markup': 'Jillian and Jackson want to know when the weather is hot and there is no rain so they can go swimming. They decide to make a circuit, with inputs H (hot) and R (rain). It outputs S (swimming). Give a Boolean expression for S.',
                               'html': '<p>Jillian and Jackson want to know when the weather is hot and there is no rain so they can go swimming. They decide to make a circuit, with inputs H (hot) and R (rain). It outputs S (swimming). Give a Boolean expression for S.</p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Andrew Waters',
                                                                               'id': 165}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Andrew Waters',
                                                                       'id': 165}]},
                                               'url': 'http://quadbase.org/questions/q14306v1',
                                               'answer_can_be_sketched': None,
                                               'id': 'q14306v1'}}, 'level': 2,
                        'id': 34},
                       {'topic': 'Expressions', 'qb_id': '14298v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '1.0', 'markup': '0',
                                'html': '<p>0</p>'},
                               {'credit': '0.0', 'markup': '1',
                                'html': '<p>1</p>'}], 'content': {
                               'markup': "Evaluate the Boolean expression:\r\n\r\n$(0+1\\cdot0+1)'$",
                               'html': "<p>Evaluate the Boolean expression:</p>\n<p>$(0+1\\cdot0+1)'$</p>"},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Andrew Waters',
                                                                               'id': 165}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Andrew Waters',
                                                                       'id': 165}]},
                                               'url': 'http://quadbase.org/questions/q14298v1',
                                               'answer_can_be_sketched': None,
                                               'id': 'q14298v1'}}, 'level': 2,
                        'id': 37},
                       {'topic': 'TT', 'qb_id': '14299v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0',
                                'markup': '0, 0, 1, 1, 0, 0, 1, 1',
                                'html': '<p>0, 0, 1, 1, 0, 0, 1, 1</p>'},
                               {'credit': '1.0',
                                'markup': '0, 1, 1, 1, 1, 0, 1, 1',
                                'html': '<p>0, 1, 1, 1, 1, 0, 1, 1</p>'},
                               {'credit': '0.0',
                                'markup': '0, 1, 0, 1, 1, 0, 1, 0',
                                'html': '<p>0, 1, 0, 1, 1, 0, 1, 0</p>'},
                               {'credit': '0.0',
                                'markup': '1, 0, 1, 1, 0, 1, 1, 1',
                                'html': '<p>1, 0, 1, 1, 0, 1, 1, 1</p>'},
                               {'credit': '0.0',
                                'markup': '1, 0, 1, 0, 0, 1, 0, 1',
                                'html': '<p>1, 0, 1, 0, 0, 1, 0, 1</p>'}],
                                               'content': {
                                                   'markup': "Let g = B+(AC'+A'C).\r\n\r\nFill in the truth table below. g for A = B = C = 0 is the first number in each answer choice; g for A = B = C = 1 is the last number.\r\n\r\n{img:truth table.PNG}",
                                                   'html': '<p>Let g = B+(AC\'+A\'C).</p>\n<p>Fill in the truth table below. g for A = B = C = 0 is the first number in each answer choice; g for A = B = C = 1 is the last number.</p>\n<p><center><img src="https://quadbase.org/system/attachments/2481/medium/8d59495fdbc4bd21381cbee411de3c92.png"></center></p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Andrew Waters',
                                                                               'id': 165}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Andrew Waters',
                                                                       'id': 165}]},
                                               'url': 'http://quadbase.org/questions/q14299v1',
                                               'answer_can_be_sketched': None,
                                               'id': 'q14299v1'}}, 'level': 3,
                        'id': 39},
                       {'topic': 'TT', 'qb_id': '14304v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '1.0',
                                'markup': "X = A'BC+AB'C+ABC'+ABC",
                                'html': "<p>X = A'BC+AB'C+ABC'+ABC</p>"},
                               {'credit': '0.0',
                                'markup': "X = A'B'C+AB'C+ABC'+ABC",
                                'html': "<p>X = A'B'C+AB'C+ABC'+ABC</p>"},
                               {'credit': '0.0',
                                'markup': "X = A'BC+AB'C+ABC'+A'B'C'",
                                'html': "<p>X = A'BC+AB'C+ABC'+A'B'C'</p>"},
                               {'credit': '0.0',
                                'markup': "X = AB'C'+A'BC'+A'B'C+A'B'C'",
                                'html': "<p>X = AB'C'+A'BC'+A'B'C+A'B'C'</p>"},
                               {'credit': '0.0',
                                'markup': "X = A'BC+AB'C+ABC'+AB'C'",
                                'html': "<p>X = A'BC+AB'C+ABC'+AB'C'</p>"}],
                                               'content': {
                                                   'markup': 'Consider the truth table below. \r\n\r\n{img:4.2.PNG}\r\n\r\nThe function X takes as input A, B, and C. Write the sum-products-Boolean expression for X.',
                                                   'html': '<p>Consider the truth table below. </p>\n<p><center><img src="https://quadbase.org/system/attachments/2487/medium/52651d4aab06c833696c5b2901a59497.png"></center></p>\n<p>The function X takes as input A, B, and C. Write the sum-products-Boolean expression for X.</p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Andrew Waters',
                                                                               'id': 165}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Andrew Waters',
                                                                       'id': 165}]},
                                               'url': 'http://quadbase.org/questions/q14304v1',
                                               'answer_can_be_sketched': None,
                                               'id': 'q14304v1'}}, 'level': 3,
                        'id': 40},
                       {'topic': 'TT', 'qb_id': '14307v2', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0',
                                'markup': '0, 1, 0, 1, 0, 1, 0, 1',
                                'html': '<p>0, 1, 0, 1, 0, 1, 0, 1</p>'},
                               {'credit': '1.0',
                                'markup': '1, 1, 0, 1, 0, 1, 0, 1',
                                'html': '<p>1, 1, 0, 1, 0, 1, 0, 1</p>'},
                               {'credit': '0.0',
                                'markup': '1, 1, 0, 0, 0, 0, 0, 0',
                                'html': '<p>1, 1, 0, 0, 0, 0, 0, 0</p>'},
                               {'credit': '0.0',
                                'markup': '0, 1, 0, 0, 0, 1, 1, 1',
                                'html': '<p>0, 1, 0, 0, 0, 1, 1, 1</p>'},
                               {'credit': '0.0',
                                'markup': '1, 1, 1, 1, 1, 1, 0, 0',
                                'html': '<p>1, 1, 1, 1, 1, 1, 0, 0</p>'}],
                                               'content': {
                                                   'markup': 'Rachel wants to use digital logic to decide when she should go to the gym. Assume that Rachel will not go if she is tired (T) or has homework (H). But she will go regardless of homework or tiredness if she is bored (B). Fill in the truth table below for G (gym).\r\n\r\n{img:4.4.prob.PNG}\r\n\r\nG for H = T = B = 0 is the first number in each answer choice; G for H = T = B = 1 is the last number.',
                                                   'html': '<p>Rachel wants to use digital logic to decide when she should go to the gym. Assume that Rachel will not go if she is tired (T) or has homework (H). But she will go regardless of homework or tiredness if she is bored (B). Fill in the truth table below for G (gym).</p>\n<p><center><img src="https://quadbase.org/system/attachments/2489/medium/c00674fcfcff4c711ee58c0fe041dd04.png"></center></p>\n<p>G for H = T = B = 0 is the first number in each answer choice; G for H = T = B = 1 is the last number.</p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Andrew Waters',
                                                                               'id': 165}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Andrew Waters',
                                                                       'id': 165}]},
                                               'url': 'http://quadbase.org/questions/q14307v2',
                                               'answer_can_be_sketched': False,
                                               'id': 'q14307v2'}}, 'level': 3,
                        'id': 43},
                       {'topic': 'Expressions', 'qb_id': '14715v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0', 'markup': '0',
                                'html': '<p>0</p>'},
                               {'credit': '1.0', 'markup': '1',
                                'html': '<p>1</p>'}], 'content': {
                               'markup': 'Evaluate the Boolean expression:\r\n\r\n1 OR 1',
                               'html': '<p>Evaluate the Boolean expression:</p>\n<p>1 OR 1</p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Phillip  Grimaldi',
                                                                               'id': 294}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Phillip  Grimaldi',
                                                                       'id': 294}]},
                                               'url': 'http://quadbase.org/questions/q14715v1',
                                               'answer_can_be_sketched': False,
                                               'id': 'q14715v1'}}, 'level': 0,
                        'id': 48},
                       {'topic': 'Expressions', 'qb_id': '14717v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '1.0', 'markup': '0',
                                'html': '<p>0</p>'},
                               {'credit': '0.0', 'markup': '1',
                                'html': '<p>1</p>'}], 'content': {
                               'markup': "Evaluate the Boolean expression:\r\n\r\n$(1\\cdot1)'$",
                               'html': "<p>Evaluate the Boolean expression:</p>\n<p>$(1\\cdot1)'$</p>"},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Phillip  Grimaldi',
                                                                               'id': 294}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Phillip  Grimaldi',
                                                                       'id': 294}]},
                                               'url': 'http://quadbase.org/questions/q14717v1',
                                               'answer_can_be_sketched': False,
                                               'id': 'q14717v1'}}, 'level': 0,
                        'id': 49},
                       {'topic': 'Expressions', 'qb_id': '14718v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '1.0', 'markup': '0',
                                'html': '<p>0</p>'},
                               {'credit': '0.0', 'markup': '1',
                                'html': '<p>1</p>'}], 'content': {
                               'markup': "Evaluate the Boolean expression:\r\n\r\n$(0+0)+(1+1)'$",
                               'html': "<p>Evaluate the Boolean expression:</p>\n<p>$(0+0)+(1+1)'$</p>"},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Phillip  Grimaldi',
                                                                               'id': 294}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Phillip  Grimaldi',
                                                                       'id': 294}]},
                                               'url': 'http://quadbase.org/questions/q14718v1',
                                               'answer_can_be_sketched': False,
                                               'id': 'q14718v1'}}, 'level': 1,
                        'id': 50},
                       {'topic': 'Circuits', 'qb_id': '14705v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0',
                                'markup': '1: OR; 2: OR; 3: AND',
                                'html': '<p>1: OR; 2: OR; 3: AND</p>'},
                               {'credit': '0.0',
                                'markup': '1: AND; 2: OR; 3: AND',
                                'html': '<p>1: AND; 2: OR; 3: AND</p>'},
                               {'credit': '0.0',
                                'markup': '1: OR; 2: AND; 3: AND',
                                'html': '<p>1: OR; 2: AND; 3: AND</p>'},
                               {'credit': '0.0',
                                'markup': '1: OR; 2: OR; 3: OR',
                                'html': '<p>1: OR; 2: OR; 3: OR</p>'},
                               {'credit': '1.0',
                                'markup': '1: AND; 2: AND; 3: OR',
                                'html': '<p>1: AND; 2: AND; 3: OR</p>'}],
                                               'content': {
                                                   'markup': "Below is an incomplete circuit that selects either $X$ or $Y$ based on the selection signal S. The final Boolean expression is: $Z = XS' + YS$.\r\n\r\n{img:mux_2.png}\r\n\r\nWhat are the logic gates that correctly complete the circuit?",
                                                   'html': '<p>Below is an incomplete circuit that selects either $X$ or $Y$ based on the selection signal S. The final Boolean expression is: $Z = XS\' + YS$.</p>\n<p><center><img src="https://quadbase.org/system/attachments/2593/medium/683d25f2dc55ecedebcd3937de2188f4.png"></center></p>\n<p>What are the logic gates that correctly complete the circuit?</p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Phillip  Grimaldi',
                                                                               'id': 294}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Phillip  Grimaldi',
                                                                       'id': 294}]},
                                               'url': 'http://quadbase.org/questions/q14705v1',
                                               'answer_can_be_sketched': False,
                                               'id': 'q14705v1'}}, 'level': 2,
                        'id': 51},
                       {'topic': 'Terminology', 'qb_id': '14713v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '1.0', 'markup': '1,0',
                                'html': '<p>1,0</p>'},
                               {'credit': '0.0', 'markup': '0,1',
                                'html': '<p>0,1</p>'}], 'content': {
                               'markup': 'Complete the following truth table: \r\n\r\n{img:NOT BLANK.png}\r\n\r\nThe first number in each answer choice refers to the first row, and the last number refers to the last row.',
                               'html': '<p>Complete the following truth table: </p>\n<p><center><img src="https://quadbase.org/system/attachments/2651/medium/228c578aeab8b1d420ed76a133037901.png"></center></p>\n<p>The first number in each answer choice refers to the first row, and the last number refers to the last row.</p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Phillip  Grimaldi',
                                                                               'id': 294}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Phillip  Grimaldi',
                                                                       'id': 294}]},
                                               'url': 'http://quadbase.org/questions/q14713v1',
                                               'answer_can_be_sketched': False,
                                               'id': 'q14713v1'}}, 'level': 0,
                        'id': 52},
                       {'topic': 'TT', 'qb_id': '14303v2', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0',
                                'markup': '0, 0, 1, 0, 1, 1, 1, 1',
                                'html': '<p>0, 0, 1, 0, 1, 1, 1, 1</p>'},
                               {'credit': '1.0',
                                'markup': '0, 0, 0, 1, 0, 1, 1, 1',
                                'html': '<p>0, 0, 0, 1, 0, 1, 1, 1</p>'},
                               {'credit': '0.0',
                                'markup': '0, 0, 1, 0, 1, 1, 1, 0',
                                'html': '<p>0, 0, 1, 0, 1, 1, 1, 0</p>'},
                               {'credit': '0.0',
                                'markup': '0, 0, 0, 1, 0, 1, 1, 0',
                                'html': '<p>0, 0, 0, 1, 0, 1, 1, 0</p>'},
                               {'credit': '0.0',
                                'markup': '0, 0, 0, 1, 1, 1, 1, 1',
                                'html': '<p>0, 0, 0, 1, 1, 1, 1, 1</p>'}],
                                               'content': {
                                                   'markup': 'Sahil wants to design a circuit that outputs 1 when at least two of the three inputs A, B, and C are 1. Fill in the truth table for this circuit, assuming that the output is X.\r\n\r\n{img:4.2.prob.PNG}\r\n\r\nX for A = B = C = 0 is the first number in each answer choice; X for A = B = C = 1 is the last number.\r\n\r\n\r\n',
                                                   'html': '<p>Sahil wants to design a circuit that outputs 1 when at least two of the three inputs A, B, and C are 1. Fill in the truth table for this circuit, assuming that the output is X.</p>\n<p><center><img src="https://quadbase.org/system/attachments/2485/medium/1e741ec00a57d42dd8bdce92bd049bea.png"></center></p>\n<p>X for A = B = C = 0 is the first number in each answer choice; X for A = B = C = 1 is the last number.</p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Andrew Waters',
                                                                               'id': 165}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Andrew Waters',
                                                                       'id': 165}]},
                                               'url': 'http://quadbase.org/questions/q14303v2',
                                               'answer_can_be_sketched': False,
                                               'id': 'q14303v2'}}, 'level': 3,
                        'id': 53},
                       {'topic': 'Terminology', 'qb_id': '14712v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0', 'markup': '1,0,0,0',
                                'html': '<p>1,0,0,0</p>'},
                               {'credit': '1.0', 'markup': '0,1,1,1',
                                'html': '<p>0,1,1,1</p>'},
                               {'credit': '0.0', 'markup': '0,1,1,0',
                                'html': '<p>0,1,1,0</p>'},
                               {'credit': '0.0', 'markup': '0,0,0,1',
                                'html': '<p>0,0,0,1</p>'}], 'content': {
                               'markup': 'Complete the following truth table: \r\n\r\n{img:OR BLANK.png}\r\n\r\nThe first number in each answer choice refers to the first row, and the last number refers to the last row.\r\n',
                               'html': '<p>Complete the following truth table: </p>\n<p><center><img src="https://quadbase.org/system/attachments/2650/medium/f13f3f0494da448750095b6286e3cbc7.png"></center></p>\n<p>The first number in each answer choice refers to the first row, and the last number refers to the last row.</p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Phillip  Grimaldi',
                                                                               'id': 294}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Phillip  Grimaldi',
                                                                       'id': 294}]},
                                               'url': 'http://quadbase.org/questions/q14712v1',
                                               'answer_can_be_sketched': False,
                                               'id': 'q14712v1'}}, 'level': 0,
                        'id': 54},
                       {'topic': 'TT', 'qb_id': '14719v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0', 'markup': "$A'+(B \\cdot C)$",
                                'html': "<p>$A'+(B \\cdot C)$</p>"},
                               {'credit': '0.0', 'markup': '$A \\cdot (B+C)$',
                                'html': '<p>$A \\cdot (B+C)$</p>'},
                               {'credit': '1.0', 'markup': '$A + (B \\cdot C)$',
                                'html': '<p>$A + (B \\cdot C)$</p>'},
                               {'credit': '0.0', 'markup': '$(A \\cdot B) + C$',
                                'html': '<p>$(A \\cdot B) + C$</p>'}],
                                               'content': {
                                                   'markup': 'Consider the truth table below:\r\n\r\n{img:truth table reverse.png}\r\n\r\nThe function g is best described by which Boolean expression?',
                                                   'html': '<p>Consider the truth table below:</p>\n<p><center><img src="https://quadbase.org/system/attachments/2652/medium/8cd17ade5c27a3778ffb16cdce46385c.png"></center></p>\n<p>The function g is best described by which Boolean expression?</p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Phillip  Grimaldi',
                                                                               'id': 294}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Phillip  Grimaldi',
                                                                       'id': 294}]},
                                               'url': 'http://quadbase.org/questions/q14719v1',
                                               'answer_can_be_sketched': False,
                                               'id': 'q14719v1'}}, 'level': 3,
                        'id': 55},
                       {'topic': 'Circuits', 'qb_id': '14315v2', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0',
                                'markup': "$M = (AB' + A'B)C+(BC+B'C')A$",
                                'html': "<p>$M = (AB' + A'B)C+(BC+B'C')A$</p>"},
                               {'credit': '0.0',
                                'markup': "$M = (AB' + A'B)C+(BC+B'C')A$",
                                'html': "<p>$M = (AB' + A'B)C+(BC+B'C')A$</p>"},
                               {'credit': '0.0',
                                'markup': '$M = (A+C) \\cdot B + (B+A) \\cdot C$',
                                'html': '<p>$M = (A+C) \\cdot B + (B+A) \\cdot C$</p>'},
                               {'credit': '1.0',
                                'markup': "$M = (A+B') \\cdot C + (B+C') \\cdot A$",
                                'html': "<p>$M = (A+B') \\cdot C + (B+C') \\cdot A$</p>"},
                               {'credit': '0.0',
                                'markup': "$M = ('A+B) \\cdot C + ('B+C) \\cdot A$",
                                'html': "<p>$M = ('A+B) \\cdot C + ('B+C) \\cdot A$</p>"}],
                                               'content': {
                                                   'markup': 'Write a Boolean expression for M.\r\n\r\n{img:updated_yuckcircuit.png}',
                                                   'html': '<p>Write a Boolean expression for M.</p>\n<p><center><img src="https://quadbase.org/system/attachments/2659/medium/7687d6e2987de05b4dbcc3c533468378.png"></center></p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Andrew Waters',
                                                                               'id': 165}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Andrew Waters',
                                                                       'id': 165}]},
                                               'url': 'http://quadbase.org/questions/q14315v2',
                                               'answer_can_be_sketched': False,
                                               'id': 'q14315v2'}}, 'level': 3,
                        'id': 56},
                       {'topic': 'Circuits', 'qb_id': '14309v2', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0',
                                'markup': 'sum: OR; products: NOT',
                                'html': '<p>sum: OR; products: NOT</p>'},
                               {'credit': '0.0',
                                'markup': 'sum: AND; products: OR',
                                'html': '<p>sum: AND; products: OR</p>'},
                               {'credit': '0.0',
                                'markup': 'sum: AND; products: AND',
                                'html': '<p>sum: AND; products: AND</p>'},
                               {'credit': '0.0',
                                'markup': 'sum: NOT; products: AND',
                                'html': '<p>sum: NOT; products: AND</p>'},
                               {'credit': '1.0',
                                'markup': 'sum: OR; products: AND',
                                'html': '<p>sum: OR; products: AND</p>'}],
                                               'content': {
                                                   'markup': 'In converting Boolean expressions to circuits, we use the sum-of products form. Which logic gate corresponds to sum, and which logic gate corresponds to products?',
                                                   'html': '<p>In converting Boolean expressions to circuits, we use the sum-of products form. Which logic gate corresponds to sum, and which logic gate corresponds to products?</p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Andrew Waters',
                                                                               'id': 165}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Andrew Waters',
                                                                       'id': 165}]},
                                               'url': 'http://quadbase.org/questions/q14309v2',
                                               'answer_can_be_sketched': False,
                                               'id': 'q14309v2'}}, 'level': 2,
                        'id': 57},
                       {'topic': 'Terminology', 'qb_id': '14448v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0', 'markup': 'Truth tables',
                                'html': '<p>Truth tables</p>'},
                               {'credit': '0.0', 'markup': 'Digital circuits',
                                'html': '<p>Digital circuits</p>'},
                               {'credit': '1.0', 'markup': 'Logic gates',
                                'html': '<p>Logic gates</p>'},
                               {'credit': '0.0', 'markup': 'None of the above',
                                'html': '<p>None of the above</p>'}],
                                               'content': {
                                                   'markup': 'Select the answer that best completes the following sentence. \r\n\r\n$\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_$ are the theoretical and electronic components that perform Boolean operations.',
                                                   'html': '<p>Select the answer that best completes the following sentence. </p>\n<p>$\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_$ are the theoretical and electronic components that perform Boolean operations.</p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Phillip  Grimaldi',
                                                                               'id': 294}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Phillip  Grimaldi',
                                                                       'id': 294}]},
                                               'url': 'http://quadbase.org/questions/q14448v1',
                                               'answer_can_be_sketched': False,
                                               'id': 'q14448v1'}}, 'level': 1,
                        'id': 58},
                       {'topic': 'TT', 'qb_id': '14314v2', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0',
                                'markup': "$X = (A' + B + C)(A + B' + C)(A + B + C')(A + B + C)$",
                                'html': "<p>$X = (A' + B + C)(A + B' + C)(A + B + C')(A + B + C)$</p>"},
                               {'credit': '1.0',
                                'markup': "$X = (A' + B' + C')(A' + B' + C)(A' + B + C')(A + B' + C')$",
                                'html': "<p>$X = (A' + B' + C')(A' + B' + C)(A' + B + C')(A + B' + C')$</p>"},
                               {'credit': '0.0',
                                'markup': "$X = (A' + B + C')(A + B' + C)(A' + B + C')(A + B + C')$",
                                'html': "<p>$X = (A' + B + C')(A + B' + C)(A' + B + C')(A + B + C')$</p>"},
                               {'credit': '0.0',
                                'markup': "$X = (A' + B + C')(A + B' + C)(A + B + C')(A + B + C)$",
                                'html': "<p>$X = (A' + B + C')(A + B' + C)(A + B + C')(A + B + C)$</p>"},
                               {'credit': '0.0',
                                'markup': "$X = A'BC + AB'C+ABC'+ABC$",
                                'html': "<p>$X = A'BC + AB'C+ABC'+ABC$</p>"}],
                                               'content': {
                                                   'markup': 'An alternative to the sum-of-products method to derive Boolean expressions from a truth table is to use a product-of-sums method. Product-of-sums works by summing the inputs that result in an output of 0, then ANDing each of these sums.\r\n\r\n{img:4.2.PNG}\r\n\r\nGive the product-of-sums representation for $X$ based on the truth table above. ',
                                                   'html': '<p>An alternative to the sum-of-products method to derive Boolean expressions from a truth table is to use a product-of-sums method. Product-of-sums works by summing the inputs that result in an output of 0, then ANDing each of these sums.</p>\n<p><center><img src="https://quadbase.org/system/attachments/2562/medium/8e8fd90f7dca8ec9108b4dc8c82790a4.png"></center></p>\n<p>Give the product-of-sums representation for $X$ based on the truth table above.</p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Andrew Waters',
                                                                               'id': 165}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Andrew Waters',
                                                                       'id': 165}]},
                                               'url': 'http://quadbase.org/questions/q14314v2',
                                               'answer_can_be_sketched': False,
                                               'id': 'q14314v2'}}, 'level': 3,
                        'id': 59},
                       {'topic': 'Expressions', 'qb_id': '14714v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0', 'markup': '1',
                                'html': '<p>1</p>'},
                               {'credit': '1.0', 'markup': '0',
                                'html': '<p>0</p>'}], 'content': {
                               'markup': 'Evaluate the Boolean expression:\r\n\r\n0 AND 0',
                               'html': '<p>Evaluate the Boolean expression:</p>\n<p>0 AND 0</p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Phillip  Grimaldi',
                                                                               'id': 294}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Phillip  Grimaldi',
                                                                       'id': 294}]},
                                               'url': 'http://quadbase.org/questions/q14714v1',
                                               'answer_can_be_sketched': False,
                                               'id': 'q14714v1'}}, 'level': 0,
                        'id': 60},
                       {'topic': 'Expressions', 'qb_id': '14716v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0', 'markup': '0',
                                'html': '<p>0</p>'},
                               {'credit': '1.0', 'markup': '1',
                                'html': '<p>1</p>'}], 'content': {
                               'markup': 'Evaluate the Boolean expression:\r\n\r\n$(1\\cdot0)+1$',
                               'html': '<p>Evaluate the Boolean expression:</p>\n<p>$(1\\cdot0)+1$</p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Phillip  Grimaldi',
                                                                               'id': 294}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Phillip  Grimaldi',
                                                                       'id': 294}]},
                                               'url': 'http://quadbase.org/questions/q14716v1',
                                               'answer_can_be_sketched': False,
                                               'id': 'q14716v1'}}, 'level': 0,
                        'id': 61},
                       {'topic': 'Terminology', 'qb_id': '14708v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0', 'markup': '1,0,0,0',
                                'html': '<p>1,0,0,0</p>'},
                               {'credit': '0.0', 'markup': '0,1,0,0',
                                'html': '<p>0,1,0,0</p>'},
                               {'credit': '0.0', 'markup': '0,0,1,0',
                                'html': '<p>0,0,1,0</p>'},
                               {'credit': '1.0', 'markup': '0,0,0,1',
                                'html': '<p>0,0,0,1</p>'}], 'content': {
                               'markup': 'Complete the following truth table: \r\n\r\n{img:AND BLANK.png}\r\n\r\nThe first number in each answer choice refers to the first row, and the last number refers to the last row.',
                               'html': '<p>Complete the following truth table: </p>\n<p><center><img src="https://quadbase.org/system/attachments/2647/medium/303ef287d3e202d89b00785020aed7e4.png"></center></p>\n<p>The first number in each answer choice refers to the first row, and the last number refers to the last row.</p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Phillip  Grimaldi',
                                                                               'id': 294}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Phillip  Grimaldi',
                                                                       'id': 294}]},
                                               'url': 'http://quadbase.org/questions/q14708v1',
                                               'answer_can_be_sketched': False,
                                               'id': 'q14708v1'}}, 'level': 0,
                        'id': 62},
                       {'topic': 'Circuits', 'qb_id': '14316v3', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0',
                                'markup': "$N = (AB' + A'B)C'(BC+B'C')A'$",
                                'html': "<p>$N = (AB' + A'B)C'(BC+B'C')A'$</p>"},
                               {'credit': '1.0',
                                'markup': "$N = ((A+B')C) \\cdot ((B+C')A)$",
                                'html': "<p>$N = ((A+B')C) \\cdot ((B+C')A)$</p>"},
                               {'credit': '0.0',
                                'markup': "$N = (AB' + A'B)C+(BC+B'C')A$",
                                'html': "<p>$N = (AB' + A'B)C+(BC+B'C')A$</p>"},
                               {'credit': '0.0',
                                'markup': "$N = ((A'+B)C) \\cdot ((B'+C)A)$",
                                'html': "<p>$N = ((A'+B)C) \\cdot ((B'+C)A)$</p>"},
                               {'credit': '0.0',
                                'markup': "$N = (AB + A'B')C \\cdot (B'C+BC)A$",
                                'html': "<p>$N = (AB + A'B')C \\cdot (B'C+BC)A$</p>"}],
                                               'content': {
                                                   'markup': 'Write a Boolean expression for $N$.\r\n\r\n{img:updated_yuckcircuit.png}',
                                                   'html': '<p>Write a Boolean expression for $N$.</p>\n<p><center><img src="https://quadbase.org/system/attachments/2660/medium/6e5ca377b9df2244901b0dfc5d166a8e.png"></center></p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Andrew Waters',
                                                                               'id': 165}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Andrew Waters',
                                                                       'id': 165}]},
                                               'url': 'http://quadbase.org/questions/q14316v3',
                                               'answer_can_be_sketched': False,
                                               'id': 'q14316v3'}}, 'level': 3,
                        'id': 63},
                       {'topic': 'Monkey', 'qb_id': '14575v2', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0',
                                'markup': '0, 0, 1, 1, 0, 0, 1, 1',
                                'html': '<p>0, 0, 1, 1, 0, 0, 1, 1</p>'},
                               {'credit': '0.0',
                                'markup': '0, 1, 1, 1, 1, 0, 1, 1',
                                'html': '<p>0, 1, 1, 1, 1, 0, 1, 1</p>'},
                               {'credit': '0.0',
                                'markup': '0, 1, 0, 1, 1, 0, 1, 0',
                                'html': '<p>0, 1, 0, 1, 1, 0, 1, 0</p>'},
                               {'credit': '1.0',
                                'markup': '0, 0, 0, 1, 0, 0, 1, 0 ',
                                'html': '<p>0, 0, 0, 1, 0, 0, 1, 0</p>'},
                               {'credit': '0.0',
                                'markup': '1, 0, 1, 0, 0, 1, 0, 1',
                                'html': '<p>1, 0, 1, 0, 0, 1, 0, 1</p>'}],
                                               'content': {
                                                   'markup': "Samir wishes to design a circuit with three inputs: A, B, and C.  He wants the circuit to output a one only if B is one and either A or C (but not both) are one.  This behavior can be represented by the Boolean expression B+(AC'+A'C).\r\n\r\nTo ensure that you are paying attention, please select option d.\r\n\r\n{img:truth table.PNG}",
                                                   'html': '<p>Samir wishes to design a circuit with three inputs: A, B, and C.  He wants the circuit to output a one only if B is one and either A or C (but not both) are one.  This behavior can be represented by the Boolean expression B+(AC\'+A\'C).</p>\n<p>To ensure that you are paying attention, please select option d.</p>\n<p><center><img src="https://quadbase.org/system/attachments/2481/medium/8d59495fdbc4bd21381cbee411de3c92.png"></center></p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Andrew Waters',
                                                                               'id': 165}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Andrew Waters',
                                                                       'id': 165}]},
                                               'url': 'http://quadbase.org/questions/q14575v2',
                                               'answer_can_be_sketched': False,
                                               'id': 'q14575v2'}}, 'level': -1,
                        'id': 64},
                       {'topic': 'Terminology', 'qb_id': '14461v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0', 'markup': 'AND',
                                'html': '<p>AND</p>'},
                               {'credit': '1.0', 'markup': 'OR',
                                'html': '<p>OR</p>'},
                               {'credit': '0.0', 'markup': 'NOT',
                                'html': '<p>NOT</p>'},
                               {'credit': '0.0', 'markup': 'NAND',
                                'html': '<p>NAND</p>'},
                               {'credit': '0.0', 'markup': 'NOR',
                                'html': '<p>NOR</p>'},
                               {'credit': '0.0', 'markup': 'XOR',
                                'html': '<p>XOR</p>'},
                               {'credit': '0.0', 'markup': 'XNOR',
                                'html': '<p>XNOR</p>'}], 'content': {
                               'markup': 'This is the electronic symbol for which logic gate?\r\n\r\n{img:2.png}',
                               'html': '<p>This is the electronic symbol for which logic gate?</p>\n<p><center><img src="https://quadbase.org/system/attachments/2614/medium/3294950035b22116d7115a0fb398c431.png"></center></p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Phillip  Grimaldi',
                                                                               'id': 294}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Phillip  Grimaldi',
                                                                       'id': 294}]},
                                               'url': 'http://quadbase.org/questions/q14461v1',
                                               'answer_can_be_sketched': False,
                                               'id': 'q14461v1'}}, 'level': 0,
                        'id': 1},
                       {'topic': 'Circuits', 'qb_id': '14312v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0', 'markup': '1: NOR; 2: AND',
                                'html': '<p>1: NOR; 2: AND</p>'},
                               {'credit': '0.0', 'markup': '1: AND; 2: OR',
                                'html': '<p>1: AND; 2: OR</p>'},
                               {'credit': '0.0', 'markup': '1: OR; 2: OR',
                                'html': '<p>1: OR; 2: OR</p>'},
                               {'credit': '0.0', 'markup': '1: NAND; 2: AND',
                                'html': '<p>1: NAND; 2: AND</p>'},
                               {'credit': '1.0', 'markup': '1: OR; 2: AND',
                                'html': '<p>1: OR; 2: AND</p>'}], 'content': {
                               'markup': 'Below is a partially completed circuit for M=A(B+C). It is missing two logic gates in the boxes. Choose the logic gates that correctly complete the circuit.\r\n\r\n{img:Selection_011.png}',
                               'html': '<p>Below is a partially completed circuit for M=A(B+C). It is missing two logic gates in the boxes. Choose the logic gates that correctly complete the circuit.</p>\n<p><center><img src="https://quadbase.org/system/attachments/2528/medium/e6085c46dd68b18aaaad902f104f1d3c.png"></center></p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Andrew Waters',
                                                                               'id': 165}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Andrew Waters',
                                                                       'id': 165}]},
                                               'url': 'http://quadbase.org/questions/q14312v1',
                                               'answer_can_be_sketched': None,
                                               'id': 'q14312v1'}}, 'level': 2,
                        'id': 2},
                       {'topic': 'Expressions', 'qb_id': '14297v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0', 'markup': '0',
                                'html': '<p>0</p>'},
                               {'credit': '1.0', 'markup': '1',
                                'html': '<p>1</p>'}], 'content': {
                               'markup': "Evaluate the Boolean expression:\r\n\r\n$1'+0'(1+(0+(1\\cdot0)))$",
                               'html': "<p>Evaluate the Boolean expression:</p>\n<p>$1'+0'(1+(0+(1\\cdot0)))$</p>"},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Andrew Waters',
                                                                               'id': 165}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Andrew Waters',
                                                                       'id': 165}]},
                                               'url': 'http://quadbase.org/questions/q14297v1',
                                               'answer_can_be_sketched': None,
                                               'id': 'q14297v1'}}, 'level': 2,
                        'id': 44},
                       {'topic': 'Expressions', 'qb_id': '14292v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '1.0', 'markup': '0',
                                'html': '<p>0</p>'},
                               {'credit': '0.0', 'markup': '1',
                                'html': '<p>1</p>'}], 'content': {
                               'markup': 'Evaluate the Boolean expression:\r\n\r\nNOT 1',
                               'html': '<p>Evaluate the Boolean expression:</p>\n<p>NOT 1</p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Andrew Waters',
                                                                               'id': 165}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Andrew Waters',
                                                                       'id': 165}]},
                                               'url': 'http://quadbase.org/questions/q14292v1',
                                               'answer_can_be_sketched': None,
                                               'id': 'q14292v1'}}, 'level': 1,
                        'id': 27},
                       {'topic': 'Expressions', 'qb_id': '14289v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0', 'markup': '1',
                                'html': '<p>1</p>'},
                               {'credit': '1.0', 'markup': '0',
                                'html': '<p>0</p>'}], 'content': {
                               'markup': 'Evaluate the Boolean expression:\r\n\r\n1 AND 0',
                               'html': '<p>Evaluate the Boolean expression:</p>\n<p>1 AND 0</p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Andrew Waters',
                                                                               'id': 165}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Andrew Waters',
                                                                       'id': 165}]},
                                               'url': 'http://quadbase.org/questions/q14289v1',
                                               'answer_can_be_sketched': None,
                                               'id': 'q14289v1'}}, 'level': 1,
                        'id': 9},
                       {'topic': 'Terminology', 'qb_id': '14460v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0', 'markup': 'AND',
                                'html': '<p>AND</p>'},
                               {'credit': '0.0', 'markup': 'OR',
                                'html': '<p>OR</p>'},
                               {'credit': '1.0', 'markup': 'NOT',
                                'html': '<p>NOT</p>'},
                               {'credit': '0.0', 'markup': 'NAND',
                                'html': '<p>NAND</p>'},
                               {'credit': '0.0', 'markup': 'NOR',
                                'html': '<p>NOR</p>'},
                               {'credit': '0.0', 'markup': 'XOR',
                                'html': '<p>XOR</p>'},
                               {'credit': '0.0', 'markup': 'XNOR',
                                'html': '<p>XNOR</p>'}], 'content': {
                               'markup': 'This is the electronic symbol for which logic gate?\r\n\r\n{img:3.png}',
                               'html': '<p>This is the electronic symbol for which logic gate?</p>\n<p><center><img src="https://quadbase.org/system/attachments/2613/medium/f172bd1e7763a558b97a29e046fe463d.png"></center></p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Phillip  Grimaldi',
                                                                               'id': 294}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Phillip  Grimaldi',
                                                                       'id': 294}]},
                                               'url': 'http://quadbase.org/questions/q14460v1',
                                               'answer_can_be_sketched': False,
                                               'id': 'q14460v1'}}, 'level': 0,
                        'id': 4},
                       {'topic': 'Expressions', 'qb_id': '14290v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0', 'markup': '0',
                                'html': '<p>0</p>'},
                               {'credit': '1.0', 'markup': '1',
                                'html': '<p>1</p>'}], 'content': {
                               'markup': 'Evaluate the Boolean expression:\r\n\r\n1 OR 0',
                               'html': '<p>Evaluate the Boolean expression:</p>\n<p>1 OR 0</p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Andrew Waters',
                                                                               'id': 165}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Andrew Waters',
                                                                       'id': 165}]},
                                               'url': 'http://quadbase.org/questions/q14290v1',
                                               'answer_can_be_sketched': None,
                                               'id': 'q14290v1'}}, 'level': 1,
                        'id': 5},
                       {'topic': 'Monkey', 'qb_id': '14575v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0',
                                'markup': '0, 0, 1, 1, 0, 0, 1, 1',
                                'html': '<p>0, 0, 1, 1, 0, 0, 1, 1</p>'},
                               {'credit': '0.0',
                                'markup': '0, 1, 1, 1, 1, 0, 1, 1',
                                'html': '<p>0, 1, 1, 1, 1, 0, 1, 1</p>'},
                               {'credit': '0.0',
                                'markup': '0, 1, 0, 1, 1, 0, 1, 0',
                                'html': '<p>0, 1, 0, 1, 1, 0, 1, 0</p>'},
                               {'credit': '1.0',
                                'markup': '0, 0, 0, 1, 0, 0, 1, 0 ',
                                'html': '<p>0, 0, 0, 1, 0, 0, 1, 0</p>'},
                               {'credit': '0.0',
                                'markup': '1, 0, 1, 0, 0, 1, 0, 1',
                                'html': '<p>1, 0, 1, 0, 0, 1, 0, 1</p>'}],
                                               'content': {
                                                   'markup': "Samir wishes to design a circuit with three inputs: A, B, and C.  He wants the circuit to output a one only if B is one and either A or C (but not both) are one.  This behavior can be represented by the Boolean expression B+(AC'+A'C).\r\n\r\nBelow is a blank truth table for the circuit along with several multiple choice options. The correct multiple choice option for this question is d. Each multiple choice option lists out the values in truth table where A = B = C = 0 corresponds to the first number in each answer choice and A = B = C = 1 corresponds to the last number.\r\n\r\nSelect the correct multiple choice option.\r\n\r\n{img:truth table.PNG}",
                                                   'html': '<p>Samir wishes to design a circuit with three inputs: A, B, and C.  He wants the circuit to output a one only if B is one and either A or C (but not both) are one.  This behavior can be represented by the Boolean expression B+(AC\'+A\'C).</p>\n<p>Below is a blank truth table for the circuit along with several multiple choice options. The correct multiple choice option for this question is d. Each multiple choice option lists out the values in truth table where A = B = C = 0 corresponds to the first number in each answer choice and A = B = C = 1 corresponds to the last number.</p>\n<p>Select the correct multiple choice option.</p>\n<p><center><img src="https://quadbase.org/system/attachments/2481/medium/8d59495fdbc4bd21381cbee411de3c92.png"></center></p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Andrew Waters',
                                                                               'id': 165}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Andrew Waters',
                                                                       'id': 165}]},
                                               'url': 'http://quadbase.org/questions/q14575v1',
                                               'answer_can_be_sketched': False,
                                               'id': 'q14575v1'}}, 'level': -1,
                        'id': 47},
                       {'topic': 'Terminology', 'qb_id': '14453v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0', 'markup': 'A AND B',
                                'html': '<p>A AND B</p>'},
                               {'credit': '1.0', 'markup': 'A OR B',
                                'html': '<p>A OR B</p>'},
                               {'credit': '0.0', 'markup': 'A NAND B',
                                'html': '<p>A NAND B</p>'},
                               {'credit': '0.0', 'markup': 'A NOR B',
                                'html': '<p>A NOR B</p>'},
                               {'credit': '0.0', 'markup': 'A XOR B',
                                'html': '<p>A XOR B</p>'},
                               {'credit': '0.0', 'markup': 'A XNOR B',
                                'html': '<p>A XNOR B</p>'}], 'content': {
                               'markup': 'A + B = ?',
                               'html': '<p>A + B = ?</p>'}, 'attribution': {
                               'license': {
                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                               'authors': [
                                   {'name': 'Phillip  Grimaldi', 'id': 294}],
                               'copyright_holders': [
                                   {'name': 'Phillip  Grimaldi', 'id': 294}]},
                                               'url': 'http://quadbase.org/questions/q14453v1',
                                               'answer_can_be_sketched': False,
                                               'id': 'q14453v1'}}, 'level': 0,
                        'id': 42},
                       {'topic': 'TT', 'qb_id': '14300v1', 'data': {
                           'simple_question': {'answer_choices': [
                               {'credit': '0.0',
                                'markup': '1, 1, 1, 0, 1, 0, 1, 1',
                                'html': '<p>1, 1, 1, 0, 1, 0, 1, 1</p>'},
                               {'credit': '1.0',
                                'markup': '1, 1, 0, 0, 0, 0, 0, 0',
                                'html': '<p>1, 1, 0, 0, 0, 0, 0, 0</p>'},
                               {'credit': '0.0',
                                'markup': '1, 0, 0, 0, 0, 0, 0, 1',
                                'html': '<p>1, 0, 0, 0, 0, 0, 0, 1</p>'},
                               {'credit': '0.0',
                                'markup': '1, 1, 0, 0, 0, 1, 1, 1',
                                'html': '<p>1, 1, 0, 0, 0, 1, 1, 1</p>'},
                               {'credit': '0.0',
                                'markup': '1, 0, 0, 0, 0, 0, 0, 0',
                                'html': '<p>1, 0, 0, 0, 0, 0, 0, 0</p>'}],
                                               'content': {
                                                   'markup': "Let g = (A+B)'(A(C+C'))'.\r\n\r\nFill in the truth table below. g for A = B = C = 0 is the first number in each answer choice; g for A = B = C = 1 is the last number.\r\n\r\n{img:truth table.PNG}\r\n ",
                                                   'html': '<p>Let g = (A+B)\'(A(C+C\'))\'.</p>\n<p>Fill in the truth table below. g for A = B = C = 0 is the first number in each answer choice; g for A = B = C = 1 is the last number.</p>\n<p><center><img src="https://quadbase.org/system/attachments/2482/medium/71d7c8da5f8b30e4e938311c9bb79e80.png"></center></p>'},
                                               'attribution': {'license': {
                                                   'name': 'Creative Commons Attribution 3.0 Unported',
                                                   'url': 'http://creativecommons.org/licenses/by/3.0/'},
                                                               'authors': [{
                                                                               'name': 'Andrew Waters',
                                                                               'id': 165}],
                                                               'copyright_holders': [
                                                                   {
                                                                       'name': 'Andrew Waters',
                                                                       'id': 165}]},
                                               'url': 'http://quadbase.org/questions/q14300v1',
                                               'answer_can_be_sketched': None,
                                               'id': 'q14300v1'}}, 'level': 3,
                        'id': 45},

                   ]
                   )


def downgrade():
    op.drop_table('assignment_sessions')
    op.drop_table('assignment_responses')
    op.drop_table('subject_assignments')
    op.drop_table('user_subjects')
    op.drop_table('roles_users')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('exercises')
