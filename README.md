# Alma Batch Vendor Delete
Scripts to check existing vendor records and then delete specified ones in bulk. (Helpful if you ended up with a bunch of junk post-migration.)

This process has two components. One to check existing vendor records for any associated order lines, and another to delete from a input spreadsheet.

Requires Acquisitions API key. Can be read-only for the record check script, but must be read/write for the vendor delete.

**Note:** Be absolutely sure you are deleting the right vendors. Changes are irreversible.

## Vendor Record Check
- Input file is the .xlsx export from the Alma Vendors list (Acquisitions->Vendors)
- Will check each vendor by code to see if there are any associated order lines (so you can make sure you're not trying to delete vendors that have orders associated with them in the system)
- Output file will include if the code was found and how many associated order lines there are

## Batch Vendor Delete
- Input file can be derived from Vendor Record Check
  - Uses only "code" and "name" as headers on input spreadsheet
- Will attempt to delete vendor with matching code
- Output file includes deletion status (including errors)
