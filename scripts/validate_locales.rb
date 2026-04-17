#!/usr/bin/env ruby
# frozen_string_literal: true

require "yaml"

LOCALES_DIR = File.expand_path("../_data/locales", __dir__)
REFERENCE_LOCALE = "en"

def node_type(value)
  case value
  when Hash
    :hash
  when Array
    :array
  else
    :scalar
  end
end

def join_path(segments)
  return "<root>" if segments.empty?

  segments.map(&:to_s).join(".")
end

def compare_types(reference, candidate, path, errors)
  reference_type = node_type(reference)
  candidate_type = node_type(candidate)

  if reference_type != candidate_type
    errors << "#{join_path(path)}: expected #{reference_type}, got #{candidate_type}"
    return
  end

  case reference
  when Hash
    reference.each do |key, reference_value|
      next unless candidate.key?(key)

      compare_types(reference_value, candidate[key], path + [key], errors)
    end
  when Array
    reference.zip(candidate).each_with_index do |(reference_value, candidate_value), index|
      next if reference_value.nil? || candidate_value.nil?

      compare_types(reference_value, candidate_value, path + [index], errors)
    end
  end
end

locale_files = Dir.glob(File.join(LOCALES_DIR, "*.yml")).sort
abort "No locale files found in #{LOCALES_DIR}" if locale_files.empty?

locales = locale_files.to_h do |path|
  [File.basename(path, ".yml"), YAML.safe_load_file(path, permitted_classes: [], aliases: false)]
end

reference = locales.fetch(REFERENCE_LOCALE) do
  abort "Missing reference locale #{REFERENCE_LOCALE}.yml"
end

failures = []

locales.each do |locale, data|
  next if locale == REFERENCE_LOCALE

  errors = []
  compare_types(reference, data, [], errors)
  next if errors.empty?

  failures << "#{locale}.yml"
  errors.each do |error|
    failures << "  - #{error}"
  end
end

if failures.empty?
  puts "Locale validation passed for #{locales.size} files."
  exit 0
end

warn "Locale validation failed:"
failures.each { |line| warn line }
exit 1
