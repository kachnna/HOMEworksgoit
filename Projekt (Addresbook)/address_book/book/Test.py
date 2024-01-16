from dataclasses import dataclass
from record import Record, Name, Phone, Email, Birthday, Address, Tag, Notes


@dataclass
class TestData:
    test_contacts = {
        1: Record(Name("Bruce Wayne"), Phone("600 123 456"), Email("bwayne@gothammail.com"), Birthday("1985-10-20"),
                  Address("174 Batman Street, Gotham City"),
                  Tag("superhero, Batman, billionaire"),
                  Notes("Bruce Wayne is the billionaire playboy philanthropist who, after witnessing his parents' murder, dedicates his life to fighting crime as the masked vigilante Batman, using his wealth and intellect to protect Gotham City."),
                  ),
        2: Record(Name("Jim Gordon"), Phone("512 987 654"), Email("jgordon@batmail.com"), Birthday("1992-03-07"),
                  Address("842 Jim Gordon Street, Gotham City"),
                  Tag("Police, justice"),
                  Notes("Commissioner James Gordon is the steadfast and honest head of the Gotham City Police Department, working tirelessly to maintain justice in a city plagued by crime and corruption."),
                  ),
        3: Record(Name("Two-face"), Phone("665 111 222"), Email("twoface@darkknightmail.com"), Birthday("1988-07-12"),
                  Address("933 Two-Face Street, Gotham City"),
                  Tag("attorney, villain"),
                  Notes("Former District Attorney Harvey Dent becomes Two-Face after a tragic accident, transforming into a split-personality criminal obsessed with duality, randomness, and making life-altering decisions with the flip of a coin."),
                  ),
        4: Record(Name("Alfred Pennyworth"), Phone("700 222 333"), Email("apennyworth@gothammail.com"), Birthday("1995-01-30"),
                  Address("Wayne's Manor 1, Gotham City"),
                  Tag("butler, assistant"),
                  Notes("Alfred Pennyworth is Bruce Wayne's loyal butler and confidant, providing emotional support, guidance, and practical assistance to Batman in his quest to save Gotham."),
                  ),
        5: Record(Name("Robin"), Phone("510 333 444"), Email("robin@batmail.com"), Birthday("1983-12-04"),
                  Address("380 Robin Street, Gotham City"),
                  Tag("sidekick, hero"),
                  Notes("Robin, often a young ward or partner to Batman, joins the Dark Knight in his crime-fighting efforts, adding youthful energy and acrobatic skills to the dynamic duo."),
                  ),
        6: Record(Name("Catwoman"), Phone("730 444 555"), Email("catwoman@batmail.com"), Birthday("1997-09-18"),
                  Address("996 Catwoman Street, Gotham City"),
                  Tag("superhero, cats"),
                  Notes("Selina Kyle, aka Catwoman, is a skilled cat burglar with a complex moral code, often walking the line between criminal and hero as she navigates her own path in Gotham City."),
                  ),
        7: Record(Name("Joker"), Phone("602 555 666"), Email("joker@gothammail.com"), Birthday("1991-06-25"),
                  Address("587 Joker Street, Gotham City"),
                  Tag("supervillain, chaos, anarchy"),
                  Notes("The Joker is an anarchic and unpredictable criminal mastermind, known for his sadistic sense of humor and obsession with creating chaos in Gotham, making him Batman's most iconic adversary."),
                  ),
        8: Record(Name("Harley Quinn"), Phone("516 666 777"), Email("hquinn@darkknightmail.com"), Birthday("1980-04-09"),
                  Address("208 Harley Quinn Street, Gotham City"),
                  Tag("villain"),
                  Notes("Formerly a psychiatrist named Dr. Harleen Quinzel, Harley Quinn becomes the Joker's devoted and unpredictable partner in crime, bringing her own brand of madness to the streets of Gotham."),
                  ),
        9: Record(Name("Penguin"), Phone("660 777 888"), Email("penguin@batmail.com"), Birthday("1994-11-19"),
                  Address("735 Penguin Street, Gotham City"),
                  Tag("villain"),
                  Notes("Oswald Cobblepot, aka the Penguin, is a cunning and stylish criminal mastermind with a penchant for bird-related gadgets and a desire for wealth and power in the criminal underworld of Gotham City."),
                  ),
        10: Record(Name("Poison Ivy"), Phone("780 888 999"), Email("poisonivy@villain.com"), Birthday("1987-08-03"),
                   Address("790 Poison Ivy Street, Gotham City"),
                   Tag("villain, flowers, ivy"),
                   Notes("Dr. Pamela Isley, known as Poison Ivy, is an eco-terrorist with a deadly touch, wielding control over plants and using her botanical prowess to defend the environment while often clashing with Gotham's heroes, particularly Batman."),
                   ),
    }

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
