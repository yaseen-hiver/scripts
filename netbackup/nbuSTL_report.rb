#!/usr/bin/ruby


=begin
# Comment Section 

This script is used to find out active NBSTL policies from NetBackup

Few assumptions
- Ruby 2.X or greater
-  Input file is called nbstl.txt
-  Last line has 72 hyphens (- * 72)

Example Run


# NbSTL.txt contains output of nbstl -L command
$ ./nbuSTL_report.rb nbstl.txt
Input File is nbstl.txt
XML Input File will be named as  nbstl.txt.xml
Following policies are active: ["slp_irb_garfield_test"]


=end

require 'optparse'
require 'rexml/document'
include REXML


inputLogFile = ARGV[0] 
puts "Input File is #{inputLogFile}\n"
xmlFileName = inputLogFile + '.xml'
puts "XML Input File will be named as  #{inputLogFile}.xml\n"


$options = {}
OptionParser.new do |opts|
  opts.banner = "Usage: reportGen [options]"
  opts.on("-v", "--verbose", "Run verbosely") do |v|
    $options[:verbose] = v
  end
end.parse!

def dprint(message)
  if $options[:verbose]
    $stderr.puts "#{Time.now}, #{message}"
  end
end

def unspacedLines(logfile, outputFile='nbstl.log')
  logLines = File.readlines(logfile)
  unspacedLines = Array.new
  logLines.each do |line|
    unspacedLines << line.strip()
 end
end


def lineSpliter(line, delimiter=':')
  dprint "I am in lineSpliter()\n"
  dprint "\tDelimiter is #{delimiter}\n"
  line = line.strip!
  key = line.split(delimiter)[0].strip.downcase.gsub(' ', '')
  value = line.split(delimiter)[1].strip.downcase
  if value =~/\(none\s{1,}specified\)/ or value =~ /\-\-/
    value = 'none'
  end
  dprint "\tKey:#{key}, \n\tValue:#{value}\n"
  return key, value
end

def genXMLTagLine(key,value)
  xmlTagLine = "<#{key}>#{value}</#{key}>"
  return xmlTagLine
end

def genXMLTags(unspacedLines)
  xmlLines = Array.new
  xmlLines << "<?xml version=\"1.0\"?>"
  xmlLines << '<netbackup>'
  unspacedLines.each do |line|
    if line.strip =~ /^Name/
      key, value = lineSpliter(line)
      xmlLines << "<policy>"
      xmlLines << genXMLTagLine(key,value)
    elsif line.strip == '-' *72
      # We need this or else it splits lines starting with '--'
       dprint "\t#{line.strip}\n"
    else
      dprint "I am in genXMLTags()\n"
      dprint "\t#{line.strip}\n"
      key, value = lineSpliter(line)
      dprint "#{key}, #{value},\n"
      dprint "\tKey:#{key}, \n\tValue:#{value}\n"
      xmlLines << genXMLTagLine(key,value)
    end

    if line.strip == '-' *72
      xmlLines << "</policy>"
    end #if block ends

  end # doLine block ends

  xmlLines << '</netbackup>'
  return xmlLines

end

formattedLines = unspacedLines(inputLogFile)
#print formattedLines
xmlLines = genXMLTags(formattedLines)

outXMLFile = File.open(xmlFileName , 'w')

xmlLines.each do |line| 
  # puts line
  outXMLFile.puts line
end

outXMLFile.close

xmlfile = File.new("nbstl.txt.xml")
doc = Document.new(xmlfile)

xmlRoot = doc.root

activePolicies = Array.new

xmlRoot.elements.each do | x |
   if x.elements["state"].text == 'active'
     activePolicies << x.elements["name"].text
   end
end


if activePolicies.size > 0
  puts "Following policies are active: #{activePolicies}"
elsif activePolicies == 0
  puts "No Active Policies were found"
end
  
