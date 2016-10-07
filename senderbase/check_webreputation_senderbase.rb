#!/usr/bin/env ruby
# This script finds the Web Reputation of a given domain using Senderbase.org
# See  http://www.senderbase.org/support/#problem=reputation for more details
#
# Author: Garfield Carneiro
# EXAMPLE1 ./check_webreputation_senderbase.rb av.com -v
# EXAMPLE2  ./check_webreputation_senderbase.rb amazon.com -v -d


require 'nokogiri'
require 'mechanize'
require 'optparse'

$options = {:domainsearch => false, :verbose => false}

parser = OptionParser.new do |opts|
  opts.banner = "Usage ./check_webreputation_senderbase.rb [options] DomainName"

  opts.on('-d', '--domain', "Search through Domain URI instead of Search String URI " ) do |domain|
       $options[:domain] = domain;
  end

  opts.on('-v', '--verbose', "Run in verbose mode for debugging") do |verbose|
    $options[:verbose] = verbose;
  end
end

parser.parse!

def dprint(message)
  if $options[:verbose]
    p message
  end
end

dprint("Options are #{$options.to_s}")

if ARGV.size == 0
  print "Pass some domain name"
  exit 4
elsif ARGV.size > 0
  dprint("Got arguments #{ARGV[0]}" )
  domainName = ARGV[0]
end

if domainName == nil
  print "Domain Name cannot be empty"
  exit 1
end

if $options[:verbose] == true
  dprint("Verbose mode : ON")
end

#By default Senderbase searches for domain in their String Search URI
#( See EXAMPLE1 at top of this file )
#but for multidatacenter domains like amazon.com we need to use Domain Search
#( See EXAMPLE2 at top of this file )

senderbaseStringSearch = 'https://www.senderbase.org/lookup/?search_string='
senderbaseDomainSearch  = 'http://www.senderbase.org/lookup/domain/?search_string='

if $options[:domain] == true
  url = senderbaseDomainSearch
else
   url = senderbaseStringSearch
 end

senderbaseQuery = url + domainName

agent  = Mechanize.new
dprint("Starting HTTP Agent #{agent.to_s}")
agent.get(senderbaseQuery)
dprint("Sending Query to Senderbase #{senderbaseQuery}")

#form contains Terms of Service (TOS)  form
form =  agent.page.form

dprint("Got form #{form.to_s}")

#Accepting TOS
form.field_with(:tos_accepted => 'Yes, I Agree')

dprint("Form buttons are #{form.buttons}")

#Submitting "Yes I Agree" button after which we get Query page
queryPage = form.submit form.buttons[0]

#doc contains HTML Code of the queryPage
doc = Nokogiri::HTML(queryPage.body)

#The CSS element with class='leftside' contains Web reputation
#HTML Code looks like <div class="leftside">Neutral</div>
rating = doc.css('div.leftside').text

dprint("We got \[#{rating.to_s.upcase}\] from Senderbase")

#If rating is Neutral or Good we are OK (Status Code 0) to Nagios
#If it is Poor we send CRITICAL (Status Code 2) to Nagios
#See  http://www.senderbase.org/support/#problem=reputation

if (rating =~ /neutral/i) or (rating =~ /good/i)
  print "OK : Web reputation for #{domainName} is #{rating}"
  exit 0
elsif (rating =~ /poor/i)
  print "ALERT : Web reputation for #{domainName} is #{rating}"
  exit 2
elsif (rating == "") or (rating.nil?)
  print "Web rating for #{domainName} not found"
  exit 3
end

