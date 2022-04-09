#!/bin/bash
#
#
cd $(dirname "$0")

currversion=$(git rev-parse --abbrev-ref HEAD)
echo $currversion
if [[ "$currversion" =~ v[0-9]\. ]]; then
	verparts=($(echo $currversion | tr "-" "\n"))
	len=${#verparts[@]}
	if [ $len -gt 1 ]; then
		txtversion=${verparts[0]}-${verparts[1]}
	else
		txtversion=${verparts[0]}
	fi
	numver=$(echo $currversion | sed -E 's/v([^-]*)/\1/')
	echo numver\: $numver
	version=$numver
	echo version\: $version

	# sed -i '' -e "s/version *= *\"[^\"]*\"/version = \"${version}\"/" $(find . -name "*.py")
	sed -i '' -e "s/version = \"[^\"]*\"/version = \"${numver}\"/" $(find . -name "*.py")
	sed -i '' -e "s/version=\"[^\"]*\"/version=\"${numver}\"/" $(find . -name "*.py")
	#	Version Test
	sed -i '' -e "s/#    Version .*/#    Version ${version}/" $(find . -name "*.py")

	git commit -m "Version ${version}" -a
	# git push

	rm -R dist/
	python3 setup*.py sdist bdist_wheel

	python3 -m twine upload dist/*${version}*

fi

cd -
