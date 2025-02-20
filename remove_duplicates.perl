#!/usr/bin/perl
use strict;

my $hash_column = 2;
$hash_column= shift @ARGV;

my $prob_column = '-';
$prob_column = shift @ARGV;

my $threshold= 0.5;
$threshold = shift @ARGV if ($#ARGV >= 0);


my $prev_hash="";

while (<>) {
    my @fields = split(/\t/, $_);
    if ($prob_column eq "-" || $fields[$prob_column] > $threshold) {
	if ($prev_hash ne $fields[$hash_column]) {
	    print $_;
	}
	$prev_hash=$fields[$hash_column];
    }
}
