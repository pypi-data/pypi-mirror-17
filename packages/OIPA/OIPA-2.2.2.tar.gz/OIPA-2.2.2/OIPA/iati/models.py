from __future__ import unicode_literals

from django.db import models
from geodata.models import Country, Region
from activity_manager import ActivityQuerySet


class ActivityDateType(models.Model):
    code = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=200)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)


class ActivityStatus(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    language = models.CharField(max_length=2)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)


class AidTypeCategory(models.Model):
    code = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)


class AidType(models.Model):
    code = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(AidTypeCategory)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)


class BudgetType(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    language = models.CharField(max_length=2)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)


class CollaborationType(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    language = models.CharField(max_length=2)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)


class ConditionType(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=40)
    language = models.CharField(max_length=2)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)


class Currency(models.Model):
    code = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=2)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)


class DescriptionType(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)


class DisbursementChannel(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.TextField()

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)

class DocumentCategoryCategory(models.Model):
    code = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=100)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)

class DocumentCategory(models.Model):
    code = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(DocumentCategoryCategory)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)

class FileFormat(models.Model):
    code = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)


class FinanceTypeCategory(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)


class FinanceType(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=220)
    category = models.ForeignKey(FinanceTypeCategory)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)


class FlowType(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    description = models.TextField()

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)


class GazetteerAgency(models.Model):
    code = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=80)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)


class GeographicalPrecision(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=80)
    description = models.TextField()

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)

class GeographicLocationClass(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=200)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)


class Language(models.Model):
    code = models.CharField(primary_key=True, max_length=2)
    name = models.CharField(max_length=80)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)

class LocationTypeCategory(models.Model):
    code = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)

class LocationType(models.Model):
    code = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=100)
    description = models.TextField(default="")
    category = models.ForeignKey(LocationTypeCategory)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)

class OrganisationIdentifier(models.Model):
    code = models.CharField(primary_key=True, max_length=20)
    abbreviation = models.CharField(max_length=30, default=None, null=True)
    name = models.CharField(max_length=250, default=None, null=True)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)


class OrganisationRole(models.Model):
    code = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=20)
    description = models.TextField()

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)


class OrganisationType(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)

class PolicyMarker(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=200)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)


class PolicySignificance(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)


class PublisherType(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)


class RelatedActivityType(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    description = models.TextField()

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)


class ResultType(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=30)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)

class SectorCategory(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)

class Sector(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(SectorCategory, null=True, default=None)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)

class TiedStatus(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=40)
    description = models.TextField()

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)


class TransactionType(models.Model):
    code = models.CharField(primary_key=True, max_length=2)
    name = models.CharField(max_length=40)
    description = models.TextField()

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)


class ValueType(models.Model):
    code = models.CharField(primary_key=True, max_length=2)
    name = models.CharField(max_length=40)
    description = models.TextField()

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)


class VerificationStatus(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)


class Vocabulary(models.Model):
    code = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=140)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)

class ActivityScope(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)

class AidTypeFlag(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)

class BudgetIdentifier(models.Model):
    code = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=160)
    category = models.CharField(max_length=120)
    sector = models.CharField(max_length=100)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)

class BudgetIdentifierSectorCategory(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=160)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)

class BudgetIdentifierSector(models.Model):
    code = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=160)
    category = models.ForeignKey(BudgetIdentifierSectorCategory)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)

class BudgetIdentifierVocabulary(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)

class ContactType(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=40)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)

class LoanRepaymentPeriod(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)

class LoanRepaymentType(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=40)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)

class RegionVocabulary(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)


class Organisation(models.Model):
    code = models.CharField(primary_key=True, max_length=80)
    abbreviation = models.CharField(max_length=80, default="")
    type = models.ForeignKey(OrganisationType, null=True, default=None)
    reported_by_organisation = models.CharField(max_length=100, default="")
    name = models.CharField(max_length=250, default="")
    original_ref = models.CharField(max_length=80, default="")

    def __unicode__(self):
        return self.name

    def total_activities(self):
        return self.activity_set.count()



class Activity(models.Model):
    hierarchy_choices = (
        (1, u"Parent"),
        (2, u"Child"),
        )

    id = models.CharField(primary_key=True, max_length=150)
    iati_identifier = models.CharField(max_length=150)
    default_currency = models.ForeignKey(Currency, null=True, default=None, related_name="default_currency")
    hierarchy = models.SmallIntegerField(choices=hierarchy_choices, default=1, null=True)
    last_updated_datetime = models.CharField(max_length=100, default="")
    linked_data_uri = models.CharField(max_length=100, default="")
    reporting_organisation = models.ForeignKey(Organisation, null=True, default=None, related_name="activity_reporting_organisation")
    secondary_publisher = models.BooleanField(default=False)
    activity_status = models.ForeignKey(ActivityStatus, null=True, default=None)

    start_planned = models.DateField(null=True, blank=True, default=None)
    end_planned = models.DateField(null=True, blank=True, default=None)
    start_actual = models.DateField(null=True, blank=True, default=None)
    end_actual = models.DateField(null=True, blank=True, default=None)

    participating_organisation = models.ManyToManyField(Organisation, through="ActivityParticipatingOrganisation")
    policy_marker = models.ManyToManyField(PolicyMarker, through="ActivityPolicyMarker")
    sector = models.ManyToManyField(Sector, through="ActivitySector")
    recipient_country = models.ManyToManyField(Country, through="ActivityRecipientCountry")
    recipient_region = models.ManyToManyField(Region, through="ActivityRecipientRegion")

    collaboration_type = models.ForeignKey(CollaborationType, null=True, default=None)
    default_flow_type = models.ForeignKey(FlowType, null=True, default=None)
    default_aid_type = models.ForeignKey(AidType, null=True, default=None)
    default_finance_type = models.ForeignKey(FinanceType, null=True, default=None)
    default_tied_status = models.ForeignKey(TiedStatus, null=True, default=None)
    xml_source_ref = models.CharField(max_length=200, default="")
    total_budget_currency = models.ForeignKey(Currency, null=True, default=None, related_name="total_budget_currency")
    total_budget = models.DecimalField(max_digits=15, decimal_places=2, null=True, default=None, db_index=True)

    capital_spend = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=None)
    scope = models.ForeignKey(ActivityScope, null=True, default=None)
    iati_standard_version = models.CharField(max_length=30, default="")

    objects = ActivityQuerySet.as_manager()

    def __unicode__(self):
        return self.id

    class Meta:
        verbose_name_plural = "activities"

class ActivitySearchData(models.Model):
    activity = models.OneToOneField(Activity)
    search_identifier = models.CharField(db_index=True, max_length=150)
    search_description = models.TextField(max_length=80000)
    search_title = models.TextField(max_length=80000)
    search_country_name = models.TextField(max_length=80000)
    search_region_name = models.TextField(max_length=80000)
    search_sector_name = models.TextField(max_length=80000)
    search_participating_organisation_name = models.TextField(max_length=80000)
    search_reporting_organisation_name = models.TextField(max_length=80000)
    search_documentlink_title = models.TextField(max_length=80000)

class ActivityParticipatingOrganisation(models.Model):
    activity = models.ForeignKey(Activity, related_name="participating_organisations")
    organisation = models.ForeignKey(Organisation, null=True, default=None)
    role = models.ForeignKey(OrganisationRole, null=True, default=None)
    name = models.TextField(default="")

    def __unicode__(self,):
        return "%s: %s - %s" % (self.activity, self.organisation, self.name)


class ActivityPolicyMarker(models.Model):
    policy_marker = models.ForeignKey(PolicyMarker, null=True, default=None)
    alt_policy_marker = models.CharField(max_length=200, default="")
    activity = models.ForeignKey(Activity)
    vocabulary = models.ForeignKey(Vocabulary, null=True, default=None)
    policy_significance = models.ForeignKey(PolicySignificance, null=True, default=None)

    def __unicode__(self,):
        return "%s - %s" % (self.activity, self.policy_marker)


class ActivitySector(models.Model):
    activity = models.ForeignKey(Activity)
    sector = models.ForeignKey(Sector, null=True, default=None)
    alt_sector_name = models.CharField(max_length=200, default="")
    vocabulary = models.ForeignKey(Vocabulary, null=True, default=None)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=None)

    def __unicode__(self,):
        return "%s - %s" % (self.activity, self.sector)


class ActivityRecipientCountry(models.Model):
    activity = models.ForeignKey(Activity)
    country = models.ForeignKey(Country)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=None)

    def __unicode__(self,):
        return "%s - %s" % (self.activity, self.country)


class CountryBudgetItem(models.Model):
    activity = models.ForeignKey(Activity)
    vocabulary = models.ForeignKey(BudgetIdentifierVocabulary, null=True)
    vocabulary_text = models.CharField(max_length=255, default="")
    code = models.CharField(max_length=50, default="")
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=None)
    description = models.TextField(default="")

    def __unicode__(self,):
        return "%s - %s" % (self.activity, self.code)


class ActivityRecipientRegion(models.Model):
    activity = models.ForeignKey(Activity)
    region = models.ForeignKey(Region)
    region_vocabulary = models.ForeignKey(RegionVocabulary, default=1)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=None)

    def __unicode__(self,):
        return "%s - %s" % (self.activity, self.region)


class OtherIdentifier(models.Model):
    activity = models.ForeignKey(Activity)
    owner_ref = models.CharField(max_length=100, default="")
    owner_name = models.CharField(max_length=100, default="")
    identifier = models.CharField(max_length=100)

    def __unicode__(self,):
        return "%s - %s" % (self.activity, self.identifier)


class ActivityWebsite(models.Model):
    activity = models.ForeignKey(Activity)
    url = models.CharField(max_length=150)

    def __unicode__(self,):
        return "%s - %s" % (self.activity, self.url)


#   Class not truly correct, attributes fully open
class ContactInfo(models.Model):
    activity = models.ForeignKey(Activity)
    person_name = models.CharField(max_length=100, default="")
    organisation = models.CharField(max_length=100, default="")
    telephone = models.CharField(max_length=100, default="")
    email = models.TextField(default="")
    mailing_address = models.TextField(default="")
    website = models.CharField(max_length=255, default="")
    contact_type = models.ForeignKey(ContactType, null=True, default=None)
    job_title = models.CharField(max_length=150, default="")

    def __unicode__(self,):
        return "%s - %s" % (self.activity, self.person_name)


class Transaction(models.Model):
    activity = models.ForeignKey(Activity)
    aid_type = models.ForeignKey(AidType, null=True, default=None)
    description = models.TextField(default="")
    description_type = models.ForeignKey(DescriptionType, null=True, default=None)
    disbursement_channel = models.ForeignKey(DisbursementChannel, null=True, default=None)
    finance_type = models.ForeignKey(FinanceType, null=True, default=None)
    flow_type = models.ForeignKey(FlowType, null=True, default=None)
    provider_organisation = models.ForeignKey(Organisation, related_name="transaction_providing_organisation", null=True, default=None)
    provider_organisation_name = models.CharField(max_length=255, default="")
    provider_activity = models.CharField(max_length=100, null=True)
    receiver_organisation = models.ForeignKey(Organisation, related_name="transaction_receiving_organisation", null=True, default=None)
    receiver_organisation_name = models.CharField(max_length=255, default="")
    tied_status = models.ForeignKey(TiedStatus, null=True, default=None)
    transaction_date = models.DateField(null=True, default=None)
    transaction_type = models.ForeignKey(TransactionType, null=True, default=None)
    value_date = models.DateField(null=True, default=None)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.ForeignKey(Currency, null=True, default=None)
    ref = models.CharField(max_length=255, default="")

    def __unicode__(self,):
        return "%s: %s - %s" % (self.activity, self.transaction_type, self.transaction_date)


# class transaction_description(models.Model):
#     transaction = models.ForeignKey(transaction)
#     type = models.ForeignKey(description_type, null=True, default=None)
#     language = models.ForeignKey(language, null=True, default=None)
#     description = models.TextField(default="")
#
#     def __unicode__(self,):
#         return "%s - %s" % (self.code, self.name)


class PlannedDisbursement(models.Model):
    activity = models.ForeignKey(Activity)
    period_start = models.CharField(max_length=100, default="")
    period_end = models.CharField(max_length=100, default="")
    value_date = models.DateField(null=True)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.ForeignKey(Currency, null=True, default=None)
    updated = models.DateField(null=True, default=None)

    def __unicode__(self,):
        return "%s - %s" % (self.activity, self.period_start)


class RelatedActivity(models.Model):
    current_activity = models.ForeignKey(Activity, related_name="related_activities")
    type = models.ForeignKey(RelatedActivityType, max_length=200, null=True, default=None)
    ref = models.CharField(max_length=200, default="")
    text = models.TextField(default="")

    def __unicode__(self,):
        return "%s - %s" % (self.current_activity, self.type)


class DocumentLink(models.Model):
    activity = models.ForeignKey(Activity)
    url = models.TextField(max_length=500)
    file_format = models.ForeignKey(FileFormat, null=True, default=None)
    document_category = models.ForeignKey(DocumentCategory, null=True, default=None)
    title = models.CharField(max_length=255, default="")

    def __unicode__(self,):
        return "%s - %s" % (self.activity, self.url)


class Result(models.Model):
    activity = models.ForeignKey(Activity, related_name="results")
    result_type = models.ForeignKey(ResultType, null=True, default=None)
    title = models.CharField(max_length=255, default="")
    description = models.TextField(default="")
    aggregation_status = models.BooleanField(default=False)

    def __unicode__(self,):
        return "%s - %s" % (self.activity, self.title)


class ResultIndicatorMeasure(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=40)

    def __unicode__(self,):
        return "%s - %s" % (self.code, self.name)


class ResultIndicator(models.Model):
    result = models.ForeignKey(Result)
    title = models.CharField(max_length=200, default="")
    description = models.TextField(default="")
    baseline_year = models.IntegerField()
    baseline_value = models.CharField(max_length=100)
    comment = models.TextField(default="")
    measure = models.ForeignKey(ResultIndicatorMeasure, null=True, default=None)

    def __unicode__(self,):
        return "%s - %s" % (self.result, self.year)

class ResultIndicatorPeriod(models.Model):
    result_indicator = models.ForeignKey(ResultIndicator)
    period_start = models.CharField(max_length=50, default="")
    period_end = models.CharField(max_length=50, default="")
    planned_disbursement_period_start = models.CharField(max_length=50, default="")
    planned_disbursement_period_end = models.CharField(max_length=50, default="")
    target = models.CharField(max_length=50, default="")
    actual = models.CharField(max_length=50, default="")

    def __unicode__(self,):
        return "%s" % (self.result_indicator)


class Title(models.Model):
    activity = models.ForeignKey(Activity)
    title = models.CharField(max_length=255, db_index=True)
    language = models.ForeignKey(Language, null=True, default=None)

    def __unicode__(self,):
        return "%s - %s" % (self.activity, self.title)


class Description(models.Model):
    activity = models.ForeignKey(Activity)
    description = models.TextField(default="", max_length=40000)
    language = models.ForeignKey(Language, null=True, default=None)
    type = models.ForeignKey(DescriptionType, related_name="description_type", null=True, default=None)
    rsr_description_type_id = models.IntegerField(null=True, default=None) # remove


    def __unicode__(self,):
        return "%s - %s" % (self.activity, self.type)


class Budget(models.Model):
    activity = models.ForeignKey(Activity)
    type = models.ForeignKey(BudgetType, null=True, default=None)
    period_start = models.CharField(max_length=50, default="")
    period_end = models.CharField(max_length=50, default="")
    value = models.DecimalField(max_digits=15, decimal_places=2)
    value_date = models.DateField(null=True, default=None)
    currency = models.ForeignKey(Currency, null=True, default=None)


    def __unicode__(self,):
        return "%s - %s" % (self.activity, self.period_start)


class Condition(models.Model):
    activity = models.ForeignKey(Activity)
    text = models.TextField(default="")
    type = models.ForeignKey(ConditionType, null=True, default=None)

    def __unicode__(self,):
        return "%s - %s" % (self.activity, self.type)

class GeographicVocabulary(models.Model):
    code = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=255)
    description = models.TextField(default="")
    category = models.CharField(max_length=50)
    url = models.TextField(default="")

    def __unicode__(self,):
        return "%s - %s" % (self.activity, self.type)

class GeographicLocationReach(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=80)

    def __unicode__(self,):
        return "%s - %s" % (self.activity, self.type)

class OrganisationRegistrationAgency(models.Model):
    code = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=160)
    description = models.TextField(default="")
    category = models.CharField(max_length=10)
    category_name = models.CharField(max_length=120)
    url = models.TextField(default="")

    def __unicode__(self,):
        return "%s - %s" % (self.activity, self.type)

class GeographicExactness(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=160)
    description = models.TextField(default="")
    category = models.CharField(max_length=50)
    url = models.TextField(default="")

    def __unicode__(self,):
        return "%s - %s" % (self.activity, self.type)

class Location(models.Model):
    activity = models.ForeignKey(Activity)
    ref = models.CharField(max_length=200, default="") # new in v1.04
    name = models.TextField(max_length=1000, default="")
    type = models.ForeignKey(LocationType, null=True, default=None, related_name="deprecated_location_type") # deprecated as of v1.04
    type_description = models.CharField(max_length=200, default="")
    description = models.TextField(default="")
    activity_description = models.TextField(default="")
    description_type = models.ForeignKey(DescriptionType, null=True, default=None)
    adm_country_iso = models.ForeignKey(Country, null=True, default=None) # deprecated as of v1.04
    adm_country_adm1 = models.CharField(max_length=100, default="") # deprecated as of v1.04
    adm_country_adm2 = models.CharField(max_length=100, default="") # deprecated as of v1.04
    adm_country_name = models.CharField(max_length=200, default="") # deprecated as of v1.04
    adm_code = models.CharField(max_length=255, default="") # new in v1.04
    adm_vocabulary = models.ForeignKey(GeographicVocabulary, null=True, default=None, related_name="administrative_vocabulary") # new in v1.04
    adm_level = models.IntegerField(null=True, default=None) # new in v1.04
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=None)
    latitude = models.CharField(max_length=70, default="") # deprecated as of v1.04
    longitude = models.CharField(max_length=70, default="") # deprecated as of v1.04
    precision = models.ForeignKey(GeographicalPrecision, null=True, default=None)
    gazetteer_entry = models.CharField(max_length=70, default="") # deprecated as of v1.04
    gazetteer_ref = models.ForeignKey(GazetteerAgency, null=True, default=None) # deprecated as of v1.04
    location_reach = models.ForeignKey(GeographicLocationReach, null=True, default=None) # new in v1.04
    location_id_vocabulary = models.ForeignKey(GeographicVocabulary, null=True, default=None, related_name="location_id_vocabulary") # new in v1.04
    location_id_code = models.CharField(max_length=255, default="") # new in v1.04
    point_srs_name = models.CharField(max_length=255, default="") # new in v1.04
    point_pos = models.CharField(max_length=255, default="") # new in v1.04
    exactness = models.ForeignKey(GeographicExactness, null=True, default=None) # new in v1.04
    feature_designation = models.ForeignKey(LocationType, null=True, default=None, related_name="feature_designation") #new in v1.04
    location_class = models.ForeignKey(GeographicLocationClass, null=True, default=None) #new in v1.04

    def __unicode__(self,):
        return "%s - %s" % (self.activity, self.name)


class Ffs(models.Model):
    activity = models.ForeignKey(Activity)
    extraction_date = models.DateField(null=True, default=None)
    priority = models.BooleanField(default=False)
    phaseout_year = models.IntegerField(null=True)

    def __unicode__(self,):
        return "%s" % (self.extraction_date)


class FfsForecast(models.Model):
    ffs = models.ForeignKey(Ffs)
    year = models.IntegerField(null=True)
    currency = models.ForeignKey(Currency)
    value_date = models.DateField(null=True, default=None)
    value = models.DecimalField(max_digits=15, decimal_places=2)

    def __unicode__(self,):
        return "%s" % (self.year)


class CrsAdd(models.Model):
    activity = models.ForeignKey(Activity)
    aid_type_flag = models.ForeignKey(AidTypeFlag)
    aid_type_flag_significance = models.IntegerField(null=True, default=None)

    def __unicode__(self,):
        return "%s" % (self.id)


class CrsAddLoanTerms(models.Model):
    crs_add = models.ForeignKey(CrsAdd)
    rate_1 = models.IntegerField(null=True, default=None)
    rate_2 = models.IntegerField(null=True, default=None)
    repayment_type = models.ForeignKey(LoanRepaymentType, null=True, default=None)
    repayment_plan = models.ForeignKey(LoanRepaymentPeriod, null=True, default=None)
    repayment_plan_text = models.TextField(default="")
    commitment_date = models.DateField(null=True, default=None)
    repayment_first_date = models.DateField(null=True, default=None)
    repayment_final_date = models.DateField(null=True, default=None)

    def __unicode__(self,):
        return "%s" % (self.crs_add_id)


class CrsAddLoanStatus(models.Model):
    crs_add = models.ForeignKey(CrsAdd)
    year = models.IntegerField(null=True, default=None)
    value_date = models.DateField(null=True, default=None)
    currency = models.ForeignKey(Currency, null=True, default=None)
    interest_received = models.DecimalField(null=True, default=None, max_digits=15, decimal_places=2)
    principal_outstanding = models.DecimalField(null=True, default=None, max_digits=15, decimal_places=2)
    principal_arrears = models.DecimalField(null=True, default=None, max_digits=15, decimal_places=2)
    interest_arrears = models.DecimalField(null=True, default=None, max_digits=15, decimal_places=2)

    def __unicode__(self,):
        return "%s" % (self.year)
