# Generated by Django 3.1.5 on 2021-03-01 07:54

import django.contrib.auth.models
import django.contrib.gis.db.models.fields
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                (
                    "note",
                    models.TextField(
                        blank=True, default="", null=True, verbose_name="Note"
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        blank=True,
                        max_length=50,
                        null=True,
                        verbose_name="Phone number",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        help_text="Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=30,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[\\w.@+ -]+$", "Enter a valid username.", "invalid"
                            )
                        ],
                        verbose_name="username",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Area",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("name", models.CharField(max_length=50, verbose_name="Area name")),
                ("note", models.TextField(verbose_name="Notes")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CompetentService",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("name", models.CharField(max_length=50, verbose_name="Name of zone")),
                (
                    "description",
                    models.TextField(verbose_name="Description of service"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="FAQ",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("question", models.TextField(verbose_name="question")),
                ("answer", models.TextField(verbose_name="answer")),
                ("order", models.IntegerField(default=1, verbose_name="Order")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="images", verbose_name="Image"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Initiative",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("MM", "MOTI ME!"),
                            ("II", "IMAM IDEJO!"),
                            ("ZM", "ZANIMA ME!"),
                        ],
                        default="MM",
                        max_length=2,
                        verbose_name="Initiative type",
                    ),
                ),
                ("title", models.CharField(max_length=50, verbose_name="Title")),
                (
                    "location",
                    django.contrib.gis.db.models.fields.PointField(
                        default="POINT(0.0 0.0)", srid=4326
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        max_length=100, verbose_name="Address of initiative"
                    ),
                ),
                ("archived", models.DateTimeField(blank=True, null=True)),
                (
                    "is_draft",
                    models.BooleanField(default=False, verbose_name="In review"),
                ),
                (
                    "area",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="initiatives",
                        to="initiatives.area",
                        verbose_name="Area",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="initiatives_initiative_author",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "cover_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="initiative_before",
                        to="initiatives.image",
                        verbose_name="Cover image before",
                    ),
                ),
                (
                    "cover_image_after",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="initiative_after",
                        to="initiatives.image",
                        verbose_name="Cover image after",
                    ),
                ),
                (
                    "publisher",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="published_initiatives",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Organization",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("name", models.CharField(max_length=50, verbose_name="name")),
                (
                    "number_of_members",
                    models.IntegerField(verbose_name="Number of members"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Rejection",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                (
                    "name",
                    models.CharField(max_length=50, verbose_name="Name of rejection"),
                ),
                ("note", models.TextField(verbose_name="Note for rejection")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Status",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("name", models.CharField(max_length=50, verbose_name="Status")),
                ("note", models.TextField(verbose_name="Default note of status")),
                (
                    "default_email",
                    models.TextField(verbose_name="Default email response"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Zone",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("name", models.CharField(max_length=50, verbose_name="Name of zone")),
                (
                    "polygon",
                    django.contrib.gis.db.models.fields.PolygonField(
                        srid=4326, verbose_name="Polygon of zone"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Vote",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="initiatives_vote_author",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "initiative",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="votes",
                        to="initiatives.initiative",
                        verbose_name="Initiative",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="StatusInitiative",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("note", models.TextField(verbose_name="Note of status")),
                ("email_content", models.TextField(verbose_name="Email response")),
                (
                    "is_email_sent",
                    models.BooleanField(default=False, verbose_name="Is email sent"),
                ),
                (
                    "competent_service",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="initiative_statuses",
                        to="initiatives.competentservice",
                        verbose_name="CompetentService",
                    ),
                ),
                (
                    "initiative",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="initiative_statuses",
                        to="initiatives.initiative",
                        verbose_name="Initiative",
                    ),
                ),
                (
                    "reason_for_rejection",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="initiatives.rejection",
                        verbose_name="Rejection",
                    ),
                ),
                (
                    "status",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="initiative_statuses",
                        to="initiatives.status",
                        verbose_name="Status of initiative",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="initiative",
            name="statuses",
            field=models.ManyToManyField(
                through="initiatives.StatusInitiative",
                to="initiatives.Status",
                verbose_name="Status of initiative",
            ),
        ),
        migrations.AddField(
            model_name="initiative",
            name="zone",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="initiatives",
                to="initiatives.zone",
                verbose_name="GEO Zone of initiative",
            ),
        ),
        migrations.CreateModel(
            name="File",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("name", models.CharField(max_length=50, verbose_name="Display name")),
                ("file", models.FileField(upload_to="files", verbose_name="File")),
                (
                    "initiative",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="files",
                        to="initiatives.initiative",
                        verbose_name="Initiative",
                    ),
                ),
                (
                    "status_initiative",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="files",
                        to="initiatives.statusinitiative",
                        verbose_name="Status Initiative",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="DescriptionDefinition",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("MM", "MOTI ME!"),
                            ("II", "IMAM IDEJO!"),
                            ("ZM", "ZANIMA ME!"),
                        ],
                        default="MM",
                        max_length=2,
                        verbose_name="Initiative type",
                    ),
                ),
                ("order", models.IntegerField(default=0)),
                ("field", models.CharField(max_length=50, verbose_name="Field name")),
                ("title", models.CharField(max_length=100, verbose_name="Title")),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="initiatives_descriptiondefinition_author",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Description",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                (
                    "field",
                    models.CharField(max_length=50, verbose_name="Description type"),
                ),
                (
                    "title",
                    models.CharField(max_length=100, verbose_name="Description title"),
                ),
                ("order", models.IntegerField(default=0)),
                ("content", models.TextField(verbose_name="Description content")),
                (
                    "initiative",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="descriptions",
                        to="initiatives.initiative",
                        verbose_name="Initiative",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "modified",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("content", models.TextField(verbose_name="Comment")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PU", "PUBLISHED"),
                            ("D", "DELETED"),
                            ("PE", "PENDING"),
                        ],
                        default="PE",
                        max_length=2,
                        verbose_name="Comment status",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="initiatives_comment_author",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "initiative",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="initiative_comments",
                        to="initiatives.initiative",
                        verbose_name="Initiative",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="area",
            name="competent_service",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="areas",
                to="initiatives.competentservice",
                verbose_name="Competent service",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="competent_services",
            field=models.ManyToManyField(
                blank=True,
                related_name="users",
                to="initiatives.CompetentService",
                verbose_name="Competent service",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                related_name="user_set",
                related_query_name="user",
                to="auth.Group",
                verbose_name="groups",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="organizations",
            field=models.ManyToManyField(
                blank=True,
                related_name="users",
                to="initiatives.Organization",
                verbose_name="Organization",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.Permission",
                verbose_name="user permissions",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="zones",
            field=models.ManyToManyField(
                blank=True,
                related_name="users",
                to="initiatives.Zone",
                verbose_name="MČ/KS",
            ),
        ),
        migrations.CreateModel(
            name="BothersInitiative",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("initiatives.initiative",),
        ),
        migrations.CreateModel(
            name="IdeaInitiative",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("initiatives.initiative",),
        ),
        migrations.CreateModel(
            name="InterestedInitiative",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("initiatives.initiative",),
        ),
        migrations.CreateModel(
            name="StatusInitiativeDone",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("initiatives.statusinitiative",),
        ),
        migrations.CreateModel(
            name="StatusInitiativeEditing",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("initiatives.statusinitiative",),
        ),
        migrations.CreateModel(
            name="StatusInitiativeFinished",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("initiatives.statusinitiative",),
        ),
        migrations.CreateModel(
            name="StatusInitiativeHear",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("initiatives.statusinitiative",),
        ),
        migrations.CreateModel(
            name="StatusInitiativeProgress",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("initiatives.statusinitiative",),
        ),
        migrations.CreateModel(
            name="StatusInitiativeRejected",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("initiatives.statusinitiative",),
        ),
    ]
