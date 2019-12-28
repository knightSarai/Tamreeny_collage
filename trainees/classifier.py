def pushup_result(push_up):
    if push_up in range(0, 11):
        return 15
    elif push_up in range(11, 21):
        return 15
    elif push_up in range(21, 31):
        return 20
    elif push_up in range(31, 41):
        return 25
    elif push_up in range(41, 51):
        return 30
    elif push_up in range(51, 61):
        return 35
    elif push_up in range(61, 81):
        return 40
    elif push_up in range(81, 100):
        return 45
    elif push_up >= 100:
        return 50


def pullup_result(pull_up):
    if pull_up in range(0, 6):
        return 5
    elif pull_up in range(6, 11):
        return 10
    elif pull_up in range(11, 16):
        return 20
    elif pull_up in range(16, 21):
        return 30
    elif pull_up in range(21, 26):
        return 40
    elif pull_up in range(26, 31):
        return 50
    elif pull_up > 30:
        return 50


def run_result(run):
    """:param run :float
    :return :int"""
    if int(run) >= 20:
        return 15
    elif int(run) in range(18, 20):
        return 20
    elif int(run) in range(16, 18):
        return 25
    elif int(run) in range(14, 16):
        return 30
    elif int(run) in range(12, 14):
        return 50
    elif int(run) < 12:
        return 50


def total_score_level(total_score):
    if total_score in range(0, 51):
        return 'beginner'
    elif total_score in range(51, 101):
        return 'intermediate'
    elif total_score in range(101, 136):
        return 'advanced'
    elif total_score > 135:
        return 'elite'


def classifier_shape(perviousLevel, classifierLevel):
    if perviousLevel == 'beginner' and classifierLevel == 'beginner':
        return False
    elif perviousLevel == classifierLevel:
        return True
    elif perviousLevel == 'beginner' and classifierLevel in ['intermediate', 'advanced', 'elite']:
        return True
    elif perviousLevel == 'intermediate' and classifierLevel in ['advanced', 'elite']:
        return True
    elif perviousLevel == 'advanced' and classifierLevel in ['elite']:
        return True
    elif perviousLevel == 'elite' and classifierLevel in ['beginner', 'intermediate', 'advanced']:
        return False
    elif perviousLevel == 'advanced' and classifierLevel in ['beginner', 'intermediate']:
        return False
    elif perviousLevel == 'intermediate' and classifierLevel == 'beginner':
        return False
