# find_in_file

**Please read carefully before running this code**

**Solution Summary:**

It was clear from the beginning, that reading through the whole file will suffer from performance issues, even when adding the optimization of reading
only the first size(search-term) characters from each line.
Reading the whole file into memory is also not feasible since the size of files does not allow it.

The suggested solution to deal with the performance and memory issue was to take advantage of the fact that the lines are ordered lexicographically and
to implement a binary search for the line that holds the requirement (>=).
The extra twist was to realize that I needed to use the stream seek / tell methods and to perform the binary search on the file byte count rather
than performing the binary search on the lines themselves in order to avoid unnecessary reads for disk.

In addition, I read the default block size information from the filesystem where the file resides and added a multiplier for the block size which 
defines the total read size performed on each read. After some experimenting I came to the conclusion the for my OS which has a default block size of 
4096, the most optimal solution was produced with a multiplier of 500. It is possible to change the multiplier in case a different block size results
in poor performance by modifying the _BLOCK_SIZE_MULTIPLIER_ parameter.

**Installation:**

This package requires a python3.8 environment with the wheel package installed.   
To install run: pip install git+https://github.com/N-o-Z/find_in_file.git  
Alternatively you can clone the repository and install locally

**Usage:**

find_in_file -h

**Testing:**

The solution was tested on several inputs:
1. Some unit testing and running provided example
2. Small input: King James version of the bible which was sorted lexicographically 
   1. File size: 4MB
   2. Search term size: small
   3. Num lines: 30382 
   4. Avg Execution time: 0.03sec
3. Medium input: Randomly generated lines of 10MB size each which were sorted lexicographically 
   1. File size: 1GB 
   2. Search term size: small
   3. Num lines: 100 
   4. Avg Execution time: 0.20sec
4. Big input: Same file as in 3 but using a 10MB input
   1. File size: 1GB 
   2. Search term size: 10MB
   3. Num lines: 100 
   4. Avg Execution time: 0.30sec


Another ~1 sec is added for the printing of the line to the screen (For 10MB lines)

**Assumptions:**

1. Using builtin comparison of strings in python - Upper case > Lower case
2. **Assuming no new line at end of file is imperative for the correct execution of this code. Please run 'truncate -s -1 <filename>' if getting bad results**
