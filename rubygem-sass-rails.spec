%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from sass-rails-3.2.5.gem by gem2rpm -*- rpm-spec -*-
%global gem_name sass-rails

Summary: Sass adapter for the Rails asset pipeline
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 4.0.3
Release: 1%{?dist}
Group: Development/Languages
License: MIT
URL: https://github.com/rails/sass-rails
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# Fix compatibility with sprockets 3.12.
# https://github.com/rails/sass-rails/commit/a62bdf85e56a678aa5fded3d4ed0d10bbc0b7a7b
Patch0: rubygem-sass-rails-4.0.3-template-instead-of-monkey-patching-spsrockets.patch
# https://github.com/rails/sass-rails/commit/bd63297c31aceb079595c3a3d9007b0e4df505b6
Patch1: rubygem-sass-rails-4.0.3-own-importer-instead-of-monkey-patching-sprockets.patch
# https://github.com/rails/sass-rails/commit/e56c2fbf60ef2bd879aae6f6163c90326b4017be
Patch2: rubygem-sass-rails-4.0.3-restore-special-behavior-in-sassimporter.patch
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix}rubygem(sass) >= 3.1.10
Requires: %{?scl_prefix}rubygem(railties) => 4.0.0
Requires: %{?scl_prefix}rubygem(railties) < 5.0.0
Requires: %{?scl_prefix}rubygem(sprockets-rails) => 2.0.0
Requires: %{?scl_prefix}rubygem(sprockets-rails) < 3.0.0
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix_ruby}rubygem(bundler)
BuildRequires: %{?scl_prefix}rubygem(sqlite3)
BuildRequires: %{?scl_prefix}rubygem(rails)
BuildRequires: %{?scl_prefix}rubygem(sass)
BuildRequires: %{?scl_prefix}rubygem(sprockets)
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

%description
Sass adapter for the Rails asset pipeline.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}.

%prep
%{?scl:scl enable %scl - << \EOF}
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}

# Use .gemspec shipped with gem, since one patch modifies the dependencies.
# gem spec %%{SOURCE0} -l --ruby > %%{gem_name}.gemspec

%patch0 -p1
%patch1 -p1
%patch2 -p1

%{?scl:EOF}


%build
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec

%gem_install
%{?scl:EOF}


%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
%{?scl:scl enable %scl - << \EOF}
set -e

pushd .%{gem_instdir}
# Use just locally available gems.
sed -i -r 's/runcmd "bundle install --verbose/\0 --local/' test/support/sass_rails_test_case.rb

# Explicitly depend on RDoc.
echo 'gem "rdoc"' >> Gemfile
sed -i '/possible_dev_dependencies/ s/%w(/%w(rdoc /' test/test_helper.rb

# Require action_controller explicitely. This should be fixed with RoR 4.1.2+.
# https://github.com/rails/sass-rails/issues/205
ruby -I.:test -raction_controller -e 'Dir.glob "test/**/*_test.rb", &method(:require)'
popd
%{?scl:EOF}


%files
%dir %{gem_instdir}
%exclude %{gem_instdir}/.*
%{gem_instdir}/MIT-LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/CHANGELOG.md
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/sass-rails.gemspec
%{gem_instdir}/sass-rails.gemspec.erb
# Leave out the test suite, since rpmlint complains a lot about dot and
# empty files.
%exclude %{gem_instdir}/test

%changelog
* Tue Jul 01 2014 Vít Ondruch <vondruch@redhat.com> - 4.0.3-1
- Update to sass-rails 4.0.3.

* Thu Oct 17 2013 Josef Stribny <jstribny@redhat.com> - 4.0.0-2
- Convert to scl

* Mon Aug 05 2013 Josef Stribny <jstribny@redhat.com> - 4.0.0-1
- Update to sass-rails 4.0.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Vít Ondruch <vondruch@redhat.com> - 3.2.6-1
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Update to sass-rails 3.2.6.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jul 23 2012 Vít Ondruch <vondruch@redhat.com> - 3.2.5-1
- Initial package
