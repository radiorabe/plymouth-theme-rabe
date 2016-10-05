%define themename rabe
%define set_theme %{_sbindir}/plymouth-set-default-theme
Name:           plymouth-theme-%{themename}
Version:        0.1
Release:        1%{?dist}
Summary:        Plymouth RaBe Theme

Group:          System Environment/Base
License:        CC-BY-SA-NC
URL:            http://www.rabe.ch
Source0:        %{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       plymouth-plugin-two-step >= 0.7.0
Requires:       plymouth-scripts

%description
This package contains the RaBe boot splash theme for Plymouth.

%prep
%setup -q

%build
# nada

%install
targetdir=$RPM_BUILD_ROOT/%{_datadir}/plymouth/themes/%{themename}
rm -rf $RPM_BUILD_ROOT
install -d -m 0755 $targetdir
install -m 0644 %{themename}.plymouth *.png $targetdir

%post
export LIB=%{_lib}
if [ $1 -eq 1 ]; then
    %{set_theme} %{themename}
fi
if [ "$(%{set_theme})" == "%{themename}" ]; then
    %{_libexecdir}/plymouth/plymouth-generate-initrd &>/dev/null
    source /etc/sysconfig/kernel &>/dev/null || :
    /sbin/new-kernel-pkg --package ${DEFAULTKERNEL:-kernel} --mkinitrd --depmod --dracut --update $(uname -r)
fi

%postun
export LIB=%{_lib}
# if uninstalling, reset to boring meatless default theme
if [ $1 -eq 0 ]; then
    if [ "$(%{set_theme})" == "%{themename}" ]; then
        %{set_theme} --reset
        %{_libexecdir}/plymouth/plymouth-generate-initrd &>/dev/null
        source /etc/sysconfig/kernel &>/dev/null || :
        /sbin/new-kernel-pkg --package ${DEFAULTKERNEL:-kernel} --mkinitrd --depmod --dracut --update $(uname -r)
    fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README.md
%dir %{_datadir}/plymouth/themes/%{themename}
%{_datadir}/plymouth/themes/%{themename}/*.png
%{_datadir}/plymouth/themes/%{themename}/%{themename}.plymouth
