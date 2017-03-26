from sys import platform
import urllib2
import os
import shutil
import tarfile
import zipfile

def main():
    proceed = raw_input('Are you sure to install/re-install elastic earch (Y/N):')
    if proceed != 'Y':
        print('Cancelling... Exiting...')
        return

    # Download link and file name across different OS
    # Reference: http://stackoverflow.com/a/8220141
    if platform == "linux" or platform == "linux2":
        # Linux
        download_link = 'https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/tar/elasticsearch/2.4.1/elasticsearch-2.4.1.tar.gz'
        source_filename = 'elasticsearch-2.4.1.tar.gz'
    elif platform == "darwin":
        # OS X
        download_link = 'https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/tar/elasticsearch/2.4.1/elasticsearch-2.4.1.tar.gz'
        source_filename = 'elasticsearch-2.4.1.tar.gz'
    elif platform == "win32":
        # Windows
        download_link = 'https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/zip/elasticsearch/2.4.1/elasticsearch-2.4.1.zip'
        source_filename = 'elasticsearch-2.4.1.zip'
    else:
        print('Unidentified OS. Terminating...')
        return

    search_dir = os.path.join(os.getcwd(), 'search')
    source_file_path = os.path.join(search_dir, source_filename)
    # Reference: http://stackoverflow.com/a/22682
    # Download
    print('Downloading ' + source_filename)
    response = urllib2.urlopen(download_link)
    with open(source_file_path, 'w') as elasticsearch_file:
        html = response.read()
        elasticsearch_file.write(html)
        response.close()

    # Extract file
    print('Extracting ' + source_filename + ' to ' + search_dir)
    elasticsearch_dir = os.path.join(search_dir, 'elasticsearch-2.4.1')
    data_dir = os.path.join(search_dir, 'data')
    logs_dir = os.path.join(search_dir, 'logs')
    if os.path.exists(elasticsearch_dir):
        shutil.rmtree(elasticsearch_dir)
    if os.path.exists(data_dir):
        shutil.rmtree(data_dir)
    if os.path.exists(logs_dir):
        shutil.rmtree(logs_dir)

    if platform == "linux" or platform == "linux2":
        # Linux
        # Reference: http://stackoverflow.com/a/31163747
        tar = tarfile.open(source_file_path)
        tar.extractall(path=search_dir)
        tar.close()
    elif platform == "darwin":
        # OS X
        tar = tarfile.open(source_file_path)
        tar.extractall(path=search_dir)
        tar.close()
    elif platform == "win32":
        # Windows
        # Reference: http://stackoverflow.com/a/3451150
        zip = zipfile.ZipFile(source_file_path)
        zip.extractall(path=search_dir)
        zip.close()

    # Configure elasticsearch
    # Reference: http://stackoverflow.com/a/39110
    print('Configuring elasticsearch')
    yml_file_path = os.path.join(os.path.join(elasticsearch_dir, 'config'), 'elasticsearch.yml')
    tmp_yml_file_path = os.path.join(os.path.join(elasticsearch_dir, 'config'), 'tmp_elasticsearch.yml')
    with open(tmp_yml_file_path, 'w') as output_file:
        with open(yml_file_path, 'r') as input_file:
            lines = input_file.read().splitlines()
        lines[66] = 'discovery.zen.ping.multicast.enabled: false'
        lines[67] = 'discovery.zen.ping.unicast.hosts: ["127.0.0.1"]'
        lines[16] = 'cluster.name: cz4034'
        lines[53] = 'network.host: 127.0.0.1'
        lines[32] = 'path.data: ' + os.path.join(search_dir, 'data')
        lines[36] = 'path.logs: ' + os.path.join(search_dir, 'logs')
        output_file.write('\n'.join(lines))

    os.remove(yml_file_path)
    shutil.move(tmp_yml_file_path, yml_file_path)
    print('Done... Exiting...')
    return


if __name__ == "__main__":
    # execute only if run as a script
    main()