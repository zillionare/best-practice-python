version=`poetry version | awk '{print $2}'`
wheel="/root/sample/sample-$version-py3-none-any.whl"
echo "packaging sample version = $version"
echo "the wheel file is $wheel"
poetry build
cp ../dist/*$version*.whl rootfs/root/sample/
docker rmi sample
docker build --build-arg version=$version --build-arg wheel=$wheel . -t sample

# launch the container
docker run -d --name sample -p 7080:7080 sample
