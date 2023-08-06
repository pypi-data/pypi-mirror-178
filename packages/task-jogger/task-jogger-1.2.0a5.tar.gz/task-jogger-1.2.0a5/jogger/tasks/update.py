import os
import shutil
import sys

from .base import Task, TaskDefinitionError, TaskError


class UpdateTask(Task):
    
    help = (
        'Update the application by checking for remote changes, pulling them '
        'if found, updating dependencies if necessary, migrating the database, '
        'collecting static files, and restarting the relevant services.'
    )
    
    temp_requirements_dir = '/tmp'
    default_branch_name = 'main'
    
    def add_arguments(self, parser):
        
        parser.add_argument(
            '--no-input',
            action='store_true',
            dest='no_input',
            help=(
                'Do not prompt for user input, e.g. to confirm dependency '
                'updates or migrations.'
            )
        )
    
    @property
    def branch_name(self):
        
        return self.settings.get('branch_name', self.default_branch_name)
    
    def handle(self, **options):
        
        self.check_updates()
        
        requirements_path, temp_requirements_path = self.check_initial_requirements()
        
        self.do_pull()
        self.do_dependency_check(requirements_path, temp_requirements_path)
        self.do_migration_check()
        self.do_stale_contenttypes_check()
        self.do_build()
        self.do_collect_static()
        self.do_restart()
        
        self.stdout.write('\nDone!', style='label')
    
    def check_updates(self):
        
        self.stdout.write('Checking for updates', style='label')
        
        # Get remote refs up to date before checking. Swallow output so it
        # isn't written to the output stream.
        update_result = self.cli('git remote update', capture=True)
        if update_result.returncode:
            self.stderr.write(update_result.stderr.decode('utf-8'))
            raise TaskError('Update check failed, could not update remotes')
        
        branch_name = self.branch_name
        log_result = self.cli(f'git log --oneline origin {branch_name}..{branch_name} | wc -l', capture=True)
        if log_result.returncode:
            self.stderr.write(log_result.stderr.decode('utf-8'))
            raise TaskError('Update check failed, could not run diff')
        
        update_count = int(log_result.stdout)
        if not update_count:
            self.stdout.write('No remote changes')
            sys.exit(0)
        
        self.stdout.write(f'Found {update_count} new remote commits')
    
    def check_initial_requirements(self):
        
        project_dir = self.project_dir
        project_name = os.path.split(project_dir)[1].replace('-', '_')
        
        requirements_path = os.path.join(project_dir, 'requirements.txt')
        temp_requirements_path = os.path.join(
            self.temp_requirements_dir,
            f'{project_name}.lastpull.requirements.txt'
        )
        
        # If this is the first time the command has been run, make a copy of
        # the requirements.txt file prior to pulling
        if not os.path.exists(temp_requirements_path):
            shutil.copyfile(requirements_path, temp_requirements_path)
        
        return requirements_path, temp_requirements_path
    
    def do_pull(self):
        
        self.stdout.write('\nPulling', style='label')
        
        branch_name = self.branch_name
        cmd = f'git pull origin {branch_name} --prune --no-rebase'
        
        result = self.cli(cmd)
        
        if result.returncode:
            # Stop script here if the pull was not successful for any reason
            raise TaskError('Pull failed')
    
    def do_dependency_check(self, requirements_path, temp_requirements_path):
        
        self.stdout.write('\nChecking Python library dependencies', style='label')
        
        # Check for dependency updates by diffing the stored requirements.txt
        # file with the one just pulled in
        diff_result = self.cli(f'diff -U 0 {temp_requirements_path} {requirements_path}', capture=True)
        
        if not diff_result.returncode:
            self.stdout.write('No changes detected')
            return
        
        # Changes were detected, show the differences and prompt the user
        # whether to proceed with an install or not. Alternatively, if running
        # in no-input mode, proceed directly to the install.
        if self.kwargs['no_input']:
            answer = 'y'
        else:
            self.stdout.write(diff_result.stdout.decode('utf-8'))
            
            answer = input(
                'The above Python library dependency changes were detected, '
                'update now (Y/n)? '
            )
        
        if answer.lower() == 'y':
            install_result = self.cli(f'pip install -r {requirements_path}')
            if install_result.returncode:
                raise TaskError('Dependency install failed')
            
            # Make a copy of the now-applied requirements.txt to compare
            # next time the task is run
            shutil.copy(requirements_path, temp_requirements_path)
        elif answer.lower() == 'n':
            self.stdout.write('Dependency update skipped', style='warning')
        else:
            # User didn't answer yes OR no, display an error message but
            # don't interrupt execution
            self.stdout.write('Dependency update aborted', style='error')
    
    def do_migration_check(self):
        
        self.stdout.write('\nChecking migrations', style='label')
        
        cmd = "python manage.py migrate --plan --check"
        
        plan_result = self.cli(cmd, capture=True)
        if not plan_result.returncode:
            self.stdout.write('No changes detected')
            return
        
        # Changes were detected, show them and prompt the user whether to
        # proceed with a migration or not. Alternatively, if running in
        # no-input mode, proceed directly with the migrations.
        if self.kwargs['no_input']:
            answer = 'y'
        else:
            self.stdout.write(plan_result.stdout.decode('utf-8'))
            answer = input('The above migrations are unapplied, apply them now (Y/n)? ')
        
        if answer.lower() == 'y':
            migrate_result = self.cli('python manage.py migrate')
            if migrate_result.returncode:
                raise TaskError('Migration failed')
        elif answer.lower() == 'n':
            self.stdout.write('Migrations skipped', style='warning')
        else:
            # User didn't answer yes OR no, display an error message but
            # don't interrupt execution
            self.stdout.write('Migrations aborted', style='error')
    
    def do_stale_contenttypes_check(self):
        
        if self.kwargs['no_input']:
            # Due to the possibility of deleting records, do not remove stale
            # content types when running in no-input mode
            return
        
        self.stdout.write('\nChecking stale content types', style='label')
        
        self.cli('python manage.py remove_stale_contenttypes')
    
    def do_build(self):
        
        try:
            proxy = self.get_task_proxy('build')
        except TaskDefinitionError:
            # A "build" task either isn't defined or is invalidly defined.
            # Do nothing.
            pass
        else:
            self.stdout.write('\nRunning build/s', style='label')
            proxy.execute()
    
    def do_collect_static(self):
        
        self.stdout.write('\nCollecting static files', style='label')
        
        cmd = 'python manage.py collectstatic'
        if self.kwargs['no_input']:
            cmd = f'{cmd} --no-input'
        
        result = self.cli(cmd)
        if result.returncode:
            raise TaskError('Static file collection failed')
    
    def do_restart(self):
        
        # Hook for subclasses to restart the necessary services after the
        # update has been completed
        pass
