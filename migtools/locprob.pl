#!/usr/bin/env perl

=pod

=head1 NAME

locprob - locate problem(s) during twiki migration

=head1 SYNOPSIS

locprob [OPTION] PATH

--help	print this help message and exit

Where I<PATH> is a path, relative or absolute is OK.

Example:

	locprob ../twiki/data/Com/Inf

=head1 DESCRIPTION

This program is intend to locate problem(s) durting twiki migration automatically

locate problems during twiki migration:

=over

=item non-prinatble char(s)

=item non-exist link(s)

=item %BB% uri encode(s)

=item title contains space

=back

=head1 AUTHOR

zhangpan05@baidu.com

=cut

use strict;
use warnings;

use Pod::Usage;
use Getopt::Long;
use URI::Escape;
use File::Spec;
use Encode;
use POSIX;

{
	#static variables
	# non-printable chars, ref: http://www.cisco.com/c/en/us/td/docs/ios/12_2/configfun/command/reference/ffun_r/frf019.pdf
	my $renpc = qr/[\x01-\x08\x10-\x1f]/;
	# not title
	my $rentt = qr/^\s*---\+{1,6}!!/;
	# title contain space
	my @respc = (qr/^\s*---\+{1,6}[^+].*?\s+[A-Z]{3,}\W.*$/,
		qr/<h[1-6] [^>]*>.*?\s+[A-Z]{3,}\W.*?<\/h[1-6]>/);
	# %BB
	my $rebbq = qr/\/[A-Za-z0-9_]*?((?:%[A-Za-z0-9]{2})*?%BB[^\]]+?)[\/\] "]/;
	# link not exist
	my $relne = qr/\[\[(?:<span[^>]*?>)+([^<]*?)(?:<\/span>)+\]/;
	# http(s) protocol
	my $rehtp = qr/https?/;
	my @tcspc = ();

	# output files:
	open(my $fhnpc, '>:encoding(UTF-8)', 'non-printable.sh') or die;
	open(my $fhspc, '>:encoding(UTF-8)', 'space-in-title.sh') or die;
	open(my $fhbbq, '>:encoding(UTF-8)', 'decode-BB.sh') or die;
	open(my $fhlne, '>:encoding(UTF-8)', 'link-not-exist.txt') or die;

	# generate shebang, prevent shell deny to exec as binary file
	print $fhnpc "#!/bin/sh\n";
	print $fhspc "#!/bin/sh\n";
	print $fhbbq "#!/bin/sh\n";

	# INPUT: file
	# OUTPUT: stdout redirect to file
	sub locprob {
		my $file = shift;
		open(my $fh, '<:encoding(UTF-8)', $file)
			or die "Could not open file [$file], $!";
		#print "processing $file\n";
		while(<$fh>) {
			chomp;
			eval { $file=decode('utf-8', $file, Encode::FB_WARN); };
			#print "processing [$file $.]\n";
			while (/($renpc)/g) {
				print $fhnpc "sed -ie '$. s/$1//' $file\n";
			}
			push @tcspc, "$_ xxxx>>>>sed -f - -i $file <<EOF\n$. {\n"
				if not (/$rentt/) and ((/$respc[0]/) or (/$respc[1]/));
			while (/$rebbq/g) {
				my $uqs = uri_unescape($1);
				my $tos = $uqs;
				{
					eval { $tos = decode('utf-8', $uqs, Encode::FB_WARN); }
					or do {
						eval {
							$tos = decode('gb2312', $uqs, Encode::FB_WARN);
						} or warn "decode %BB quote failed: $uqs";
					}
				}
				print $fhbbq "sed -ie '$. s/$1/$tos/' $file\n";
			}
			if (/$relne/ and $1 !~ /$rehtp/) {
				my @tfpts = File::Spec->splitpath($1);
				my @ofpts = File::Spec->splitpath($file);
				$ofpts[$#ofpts] = $tfpts[$#tfpts] . '.txt';
				my $lnkf = File::Spec->catpath(@ofpts);
				print $fhlne "link not exists found: [$file $.] $1 -> $lnkf\n"
					if (! -f $lnkf);
			}
		}
	} # end-of-locprob

	# locate title contains space problem and generate autofix script
	sub loctcs {
		my @ufn = @_;
		my $proc;
		foreach my $line (@tcspc) {
			$proc = 0;
			foreach (@ufn) {
				if (index($line, " $_") != -1) {
					$line .= "s/ $_/\\\&nbsp\\\;$_/g\n";
					$proc = 1;
				}
			}
			$line =~ s/^.*xxxx>>>>//;
			$line .= "}\nEOF\n";
			print $fhspc $line if $proc;
		}
	}
}

#sub main
{
	# Parse options and print usage if there is a syntax error,
	# or if usage was explicitly requested.
	my $help = 0;
	GetOptions('help|h' => \$help) or pod2usage(2);
	pod2usage(1) if $help or @ARGV != 1;
	my $path = shift;
	die "Invalid directory: [$path]" unless -d $path;

	#binmode(STDOUT, ':encoding(UTF-8)');
	my @fa = <$path/*.txt{,\\,v}>;
	my @ufn = ();
	my $ufn = qr/\/([A-Z]{3,}).txt$/;
	print strftime('%F %T', localtime()) . " Process begin\n";
	# detect all uppercase filename, 3 letters at least
	foreach (@fa) {
		push @ufn, $1 if (/$ufn/);
	}
	foreach (@fa) {
		&locprob($_);
	}
	&loctcs(@ufn);
	print strftime('%F %T', localtime()) . " Process end\n";
}

# vim: ts=4 sw=4
