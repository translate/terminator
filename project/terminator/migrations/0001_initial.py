# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdministrativeStatus',
            fields=[
                ('name', models.CharField(max_length=20, verbose_name='name')),
                ('tbx_representation', models.CharField(max_length=25, serialize=False, verbose_name='TBX representation', primary_key=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('allows_administrative_status_reason', models.BooleanField(default=False, verbose_name='allows setting administrative status reason')),
            ],
            options={
                'verbose_name': 'administrative status',
                'verbose_name_plural': 'administrative statuses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AdministrativeStatusReason',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40, verbose_name='name')),
                ('description', models.TextField(verbose_name='description')),
            ],
            options={
                'verbose_name': 'administrative status reason',
                'verbose_name_plural': 'administrative status reasons',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CollaborationRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('collaboration_role', models.CharField(max_length=2, verbose_name='collaboration role', choices=[('O', 'Glossary owner'), ('L', 'Lexicographer'), ('T', 'Terminologist')])),
                ('sent_date', models.DateTimeField(auto_now_add=True, verbose_name='sent date')),
            ],
            options={
                'verbose_name': 'collaboration request',
                'verbose_name_plural': 'collaboration requests',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Concept',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('broader_concept', models.ForeignKey(related_name='narrower_concepts', on_delete=django.db.models.deletion.PROTECT, verbose_name='broader concept', blank=True, to='terminator.Concept', null=True)),
            ],
            options={
                'verbose_name': 'concept',
                'verbose_name_plural': 'concepts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConceptLanguageCommentsThread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('concept', models.ForeignKey(to='terminator.Concept')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContextSentence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=250, verbose_name='text')),
            ],
            options={
                'verbose_name': 'context sentence',
                'verbose_name_plural': 'context sentences',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CorpusExample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.URLField(verbose_name='address')),
                ('description', models.TextField(verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name': 'corpus example',
                'verbose_name_plural': 'corpus examples',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Definition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('definition_text', models.TextField(verbose_name='definition text')),
                ('is_finalized', models.BooleanField(default=False, verbose_name='is finalized')),
                ('source', models.URLField(verbose_name='source', blank=True)),
                ('concept', models.ForeignKey(verbose_name='concept', to='terminator.Concept')),
            ],
            options={
                'verbose_name': 'definition',
                'verbose_name_plural': 'definitions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExternalLinkType',
            fields=[
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('tbx_representation', models.CharField(max_length=30, serialize=False, verbose_name='TBX representation', primary_key=True)),
                ('description', models.TextField(verbose_name='description')),
            ],
            options={
                'verbose_name': 'external link type',
                'verbose_name_plural': 'external link types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExternalResource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.URLField(verbose_name='address')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('concept', models.ForeignKey(verbose_name='concept', to='terminator.Concept')),
            ],
            options={
                'verbose_name': 'external resource',
                'verbose_name_plural': 'external resources',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Glossary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name='name')),
                ('description', models.TextField(verbose_name='description')),
                ('subject_fields', models.ManyToManyField(related_name='glossary_subject_fields', null=True, verbose_name='subject fields', to='terminator.Concept', blank=True)),
                ('subscribers', models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True, verbose_name='subscribers', blank=True)),
            ],
            options={
                'verbose_name': 'glossary',
                'verbose_name_plural': 'glossaries',
                'permissions': (('is_terminologist_in_this_glossary', 'Is terminologist in this glossary'), ('is_lexicographer_in_this_glossary', 'Is lexicographer in this glossary'), ('is_owner_for_this_glossary', 'Is owner for this glossary')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GrammaticalGender',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('tbx_representation', models.CharField(max_length=100, verbose_name='TBX representation')),
                ('description', models.TextField(verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name': 'grammatical gender',
                'verbose_name_plural': 'grammatical genders',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GrammaticalNumber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('tbx_representation', models.CharField(max_length=100, verbose_name='TBX representation')),
                ('description', models.TextField(verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name': 'grammatical number',
                'verbose_name_plural': 'grammatical numbers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('iso_code', models.CharField(max_length=10, serialize=False, verbose_name='ISO code', primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('description', models.TextField(verbose_name='description')),
                ('grammatical_genders', models.ManyToManyField(to='terminator.GrammaticalGender', verbose_name='grammatical genders')),
                ('grammatical_numbers', models.ManyToManyField(to='terminator.GrammaticalNumber', verbose_name='grammatical numbers')),
            ],
            options={
                'verbose_name': 'language',
                'verbose_name_plural': 'languages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PartOfSpeech',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('tbx_representation', models.CharField(max_length=100, verbose_name='TBX representation')),
                ('description', models.TextField(verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name': 'part of speech',
                'verbose_name_plural': 'parts of speech',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PartOfSpeechForLanguage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('allows_grammatical_gender', models.BooleanField(default=False, verbose_name='allows grammatical gender')),
                ('allows_grammatical_number', models.BooleanField(default=False, verbose_name='allows grammatical number')),
                ('language', models.ForeignKey(verbose_name='language', to='terminator.Language')),
                ('part_of_speech', models.ForeignKey(verbose_name='part of speech', to='terminator.PartOfSpeech')),
            ],
            options={
                'verbose_name_plural': 'parts of speech for languages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('word', models.CharField(max_length=100, verbose_name='word')),
                ('definition', models.TextField(verbose_name='definition')),
                ('sent_date', models.DateTimeField(auto_now_add=True, verbose_name='sent date')),
                ('for_glossary', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='for glossary', to='terminator.Glossary')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='language', to='terminator.Language')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='user', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'proposal',
                'verbose_name_plural': 'proposals',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SummaryMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(verbose_name='summary message text')),
                ('is_finalized', models.BooleanField(default=False, verbose_name='is finalized')),
                ('date', models.DateTimeField(auto_now=True)),
                ('concept', models.ForeignKey(verbose_name='concept', to='terminator.Concept')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='language', to='terminator.Language')),
            ],
            options={
                'verbose_name': 'summary message',
                'verbose_name_plural': 'summary messages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('translation_text', models.CharField(max_length=100, verbose_name='translation text')),
                ('process_status', models.BooleanField(default=False, verbose_name='Is finalized')),
                ('note', models.TextField(blank=True)),
                ('administrative_status', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='administrative status', blank=True, to='terminator.AdministrativeStatus', null=True)),
                ('administrative_status_reason', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='administrative status reason', blank=True, to='terminator.AdministrativeStatusReason', null=True)),
                ('concept', models.ForeignKey(verbose_name='concept', to='terminator.Concept')),
                ('grammatical_gender', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='grammatical gender', blank=True, to='terminator.GrammaticalGender', null=True)),
                ('grammatical_number', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='grammatical number', blank=True, to='terminator.GrammaticalNumber', null=True)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='language', to='terminator.Language')),
                ('part_of_speech', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='part of speech', blank=True, to='terminator.PartOfSpeech', null=True)),
            ],
            options={
                'ordering': ['concept', 'language'],
                'verbose_name': 'translation',
                'verbose_name_plural': 'translations',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='summarymessage',
            unique_together=set([('concept', 'language')]),
        ),
        migrations.AlterUniqueTogether(
            name='partofspeechforlanguage',
            unique_together=set([('language', 'part_of_speech')]),
        ),
        migrations.AddField(
            model_name='language',
            name='parts_of_speech',
            field=models.ManyToManyField(to='terminator.PartOfSpeech', verbose_name='parts of speech', through='terminator.PartOfSpeechForLanguage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='externalresource',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='language', to='terminator.Language'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='externalresource',
            name='link_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='link type', to='terminator.ExternalLinkType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='definition',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='language', to='terminator.Language'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='definition',
            unique_together=set([('concept', 'language')]),
        ),
        migrations.AddField(
            model_name='corpusexample',
            name='translation',
            field=models.ForeignKey(verbose_name='translation', to='terminator.Translation'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='corpusexample',
            unique_together=set([('translation', 'address')]),
        ),
        migrations.AddField(
            model_name='contextsentence',
            name='translation',
            field=models.ForeignKey(verbose_name='translation', to='terminator.Translation'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='contextsentence',
            unique_together=set([('translation', 'text')]),
        ),
        migrations.AddField(
            model_name='conceptlanguagecommentsthread',
            name='language',
            field=models.ForeignKey(to='terminator.Language', on_delete=django.db.models.deletion.PROTECT),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='conceptlanguagecommentsthread',
            unique_together=set([('concept', 'language')]),
        ),
        migrations.AddField(
            model_name='concept',
            name='glossary',
            field=models.ForeignKey(verbose_name='glossary', to='terminator.Glossary'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='concept',
            name='related_concepts',
            field=models.ManyToManyField(related_name='related_concepts_rel_+', null=True, verbose_name='related concepts', to='terminator.Concept', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='concept',
            name='subject_field',
            field=models.ForeignKey(related_name='concepts_in_subject_field', on_delete=django.db.models.deletion.PROTECT, verbose_name='subject field', blank=True, to='terminator.Concept', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='collaborationrequest',
            name='for_glossary',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='for glossary', to='terminator.Glossary'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='collaborationrequest',
            name='user',
            field=models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='collaborationrequest',
            unique_together=set([('user', 'for_glossary', 'collaboration_role')]),
        ),
        migrations.AddField(
            model_name='administrativestatusreason',
            name='languages',
            field=models.ManyToManyField(to='terminator.Language', verbose_name='languages'),
            preserve_default=True,
        ),
    ]
