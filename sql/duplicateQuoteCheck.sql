SELECT text, COUNT(*) occurrences FROM quote GROUP BY text HAVING occurrences > 1;
