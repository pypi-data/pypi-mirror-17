import click

import os.path
from chisubmit.common import CHISUBMIT_SUCCESS, CHISUBMIT_FAIL
from chisubmit.cli.common import create_grading_repos,\
    gradingrepo_push_grading_branch, gradingrepo_pull_grading_branch,\
    get_grader_or_exit, get_assignment_or_exit, get_teams_registrations,\
    catch_chisubmit_exceptions, require_local_config
from chisubmit.repos.grading import GradingGitRepo
from chisubmit.rubric import RubricFile, ChisubmitRubricException
from chisubmit.cli.common import pass_course
from chisubmit.cli.shared.course import shared_course_get_git_credentials


@click.group()
@click.pass_context
def grader(ctx):
    pass

@click.command(name="create-local-grading-repos")
@click.option('--grader', type=str)
@click.argument('assignment_id', type=str)
@catch_chisubmit_exceptions
@require_local_config
@pass_course
@click.pass_context
def grader_create_local_grading_repos(ctx, course, grader, assignment_id):
    if grader is None:
        user = ctx.obj["client"].get_user()    
        
        grader = get_grader_or_exit(ctx, course, user.username)
    else:
        grader = get_grader_or_exit(ctx, course, grader)
        
    assignment = get_assignment_or_exit(ctx, course, assignment_id)

    teams_registrations = get_teams_registrations(course, assignment, grader = grader)
    
    if len(teams_registrations) == 0:
        print "No teams found"
        ctx.exit(CHISUBMIT_FAIL)

    repos = create_grading_repos(ctx.obj['config'], course, assignment, teams_registrations)

    for repo in repos:
        repo.set_grader_author()

    for team, registration in teams_registrations.items():
        print ("Pulling grading branch for team %s... " % team.team_id),
        gradingrepo_pull_grading_branch(ctx.obj['config'], course, team, registration, from_staging = True)
        print "done"
        
    return CHISUBMIT_SUCCESS

def validate_repo_rubric(ctx, course, assignment, team, registration):
    repo = GradingGitRepo.get_grading_repo(ctx.obj['config'], course, team, registration)
    if not repo:
        print "Repository for %s does not exist" % (team.team_id)
        ctx.exit(CHISUBMIT_FAIL)

    rubricfile = repo.repo_path + "/%s.rubric.txt" % assignment.assignment_id

    if not os.path.exists(rubricfile):
        print "Repository for %s does not exist have a rubric for assignment %s" % (team.team_id, assignment.assignment_id)
        ctx.exit(CHISUBMIT_FAIL)

    try:
        RubricFile.from_file(open(rubricfile), assignment)
        return (True, None)
    except ChisubmitRubricException, cre:
        return (False, cre.message)


@click.command(name="validate-rubrics")
@click.argument('assignment_id', type=str)
@click.option('--grader', type=str)
@click.option('--only', type=str)
@catch_chisubmit_exceptions
@require_local_config
@pass_course
@click.pass_context
def grader_validate_rubrics(ctx, course, assignment_id, grader, only):
    if grader is None:
        user = ctx.obj["client"].get_user()    
        
        grader = get_grader_or_exit(ctx, course, user.username)
    else:
        grader = get_grader_or_exit(ctx, course, grader)

    assignment = get_assignment_or_exit(ctx, course, assignment_id)

    teams_registrations = get_teams_registrations(course, assignment, grader = grader, only = only)
    
    for team, registration in teams_registrations.items():
        valid, error_msg = validate_repo_rubric(ctx, course, assignment, team, registration)

        if valid:
            print "%s: Rubric OK." % team.team_id
        else:
            print "%s: Rubric ERROR: %s" % (team.team_id, error_msg)

    return CHISUBMIT_SUCCESS


@click.command(name="push-grading-branches")
@click.argument('assignment_id', type=str)
@click.option('--grader', type=str)
@click.option('--only', type=str)
@click.option('--skip-rubric-validation', is_flag=True)
@require_local_config
@pass_course
@click.pass_context
def grader_push_grading_branches(ctx, course, assignment_id, grader, only, skip_rubric_validation):
    if grader is None:
        user = ctx.obj["client"].get_user()    
        
        grader = get_grader_or_exit(ctx, course, user.username)
    else:
        grader = get_grader_or_exit(ctx, course, grader)

    assignment = get_assignment_or_exit(ctx, course, assignment_id)

    teams_registrations = get_teams_registrations(course, assignment, grader = grader, only = only, only_ready_for_grading=True)
    
    if len(teams_registrations) == 0:
        print "No teams found"
        ctx.exit(CHISUBMIT_FAIL)

    for team, registration in teams_registrations.items():
        if not skip_rubric_validation:
            valid, error_msg = validate_repo_rubric(ctx, course, assignment, team, registration)
            if not valid:
                print "Not pushing branch for team %s. Rubric does not validate: %s" % (team.team_id, error_msg)
                continue
        
        print "Pushing grading branch for team %s... " % team.team_id
        gradingrepo_push_grading_branch(ctx.obj['config'], course, team, registration, to_staging = True)

    return CHISUBMIT_SUCCESS

@click.command(name="pull-grading-branches")
@click.argument('assignment_id', type=str)
@click.option('--grader', type=str)
@click.option('--only', type=str)
@catch_chisubmit_exceptions
@require_local_config
@pass_course
@click.pass_context
def grader_pull_grading_branches(ctx, course, assignment_id, grader, only):
    if grader is None:
        user = ctx.obj["client"].get_user()    
        
        grader = get_grader_or_exit(ctx, course, user.username)
    else:
        grader = get_grader_or_exit(ctx, course, grader)

    assignment = get_assignment_or_exit(ctx, course, assignment_id)

    teams_registrations = get_teams_registrations(course, assignment, grader = grader, only = only, only_ready_for_grading=True)
    
    if len(teams_registrations) == 0:
        print "No teams found"
        ctx.exit(CHISUBMIT_FAIL)

    for team, registration in teams_registrations.items():
        print "Pulling grading branch for team %s... " % team.team_id
        gradingrepo_pull_grading_branch(ctx.obj['config'], course, team, registration, from_staging = True)

    return CHISUBMIT_SUCCESS

grader.add_command(grader_create_local_grading_repos)
grader.add_command(grader_validate_rubrics)
grader.add_command(grader_push_grading_branches)
grader.add_command(grader_pull_grading_branches)
grader.add_command(shared_course_get_git_credentials)

