from django.db import models

# Create your models here.
class Voter(models.Model):
    '''Store a representation of voters'''
    # Personal information
    voterID = models.TextField()
    last_name = models.TextField()
    first_name = models.TextField()
    street_number = models.TextField()
    street_name = models.TextField()
    apartment_number = models.TextField(blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.TextField()
    precinct_number = models.TextField()
    
    # Election participation fields
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    
    # Score for voter participation
    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.party_affiliation})"

def load_data(filename):
    '''Function to load data records from CSV file into Voter model instances.'''
    
    # Delete existing records to prevent duplicates
    Voter.objects.all().delete()
    
    filename = '/Users/kevintan/Desktop/django/voter_analytics/newton_voters.csv'
    f = open(filename)
    f.readline()

    for line in f:
        row = line.split(',')
        
        try:
            voter = Voter(
                voterID=row[0],
                last_name=row[1],
                first_name=row[2],
                street_number=row[3],
                street_name=row[4],
                apartment_number=row[5] if row[5] else None,
                zip_code=row[6],
                date_of_birth=row[7],
                date_of_registration=row[8],
                party_affiliation=row[9],
                precinct_number=row[10],
                v20state=row[11] == 'TRUE',
                v21town=row[12] == 'TRUE',
                v21primary=row[13] == 'TRUE',
                v22general=row[14] == 'TRUE',
                v23town=row[15] == 'TRUE',
                voter_score=int(row[16]),
            )
            voter.save()  # Save this instance to the database
            print(f'Created voter: {voter.first_name} {voter.last_name}')
    
        except Exception as e:
            print(f"Exception on {row}: {e}")
    
    print(f'Done. Created {Voter.objects.count()} Voters.')
