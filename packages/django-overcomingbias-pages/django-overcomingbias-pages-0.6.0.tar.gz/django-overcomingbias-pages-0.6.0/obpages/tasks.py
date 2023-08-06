from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from huey.contrib.djhuey import task
from obapi.models import OBContentItem


@task()
def download_new_items():
    """Task which downloads new overcomingbias posts.

    Provide the user_pk argument if you want the additions to be logged in the admin
    site.
    """
    OBContentItem.objects.download_new_items()


@task()
def update_edited_items(user_pk=None):
    """Task which downloads new overcomingbias posts.

    Provide the user_pk argument if you want the additions to be logged in the admin
    site.
    """
    updated_items = OBContentItem.objects.update_edited_items()

    # Log item changes if user pk is provided
    if user_pk:
        content_type_pk = ContentType.objects.get_for_model(OBContentItem).pk
        for item in updated_items:
            LogEntry.objects.log_action(
                user_id=user_pk,
                content_type_id=content_type_pk,
                object_id=item.pk,
                object_repr=str(item),
                action_flag=CHANGE,
                change_message=f"Updated item {item}",
            )


@task()
def update_search_index():
    action = "update_index"
    args = ["--remove"]
    call_command(action, *args)


@task()
def rebuild_search_index():
    action = "rebuild_index"
    args = ["--noinput"]
    call_command(action, *args)
