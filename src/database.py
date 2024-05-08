"""Placeholder idea for now.

In order to provide colon lookup for the user, we can either search a text for
given cola on demand (lengthy process, depending on the size of the text), or 
else set up the service by pre-parsing the corpus and using a database for lookup
(a very lengthy process, but only needs to be done once, or whenever the parser 
changes in a significant way). The middle ground is to parse texts on demand, but
write them to the database when we are done parsing, so they can be looked up easier
later.



colon type -> {locus: lemma}


"""