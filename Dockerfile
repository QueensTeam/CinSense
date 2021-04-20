### 1. Get Linux
FROM centos:7

### 2. Get Java via the package manager
RUN rpm --import https://yum.corretto.aws/corretto.key 
RUN curl -L -o /etc/yum.repos.d/corretto.repo https://yum.corretto.aws/corretto.repo


RUN yum update -y \
&& yum install -y java-15-amazon-corretto-devel -y \
&& yum clean all \
&& rm -rf /var/cache/yum

# Set JAVA_HOME environment var
ENV JAVA_HOME="/usr/lib/jvm/jre-openjdk"

# Install Python
RUN yum install python3 -y \
&& pip3 install --upgrade pip setuptools wheel \
&& if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi \
&& if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi \
&& yum clean all \
&& rm -rf /var/cache/yum


### Get Flask for the app
RUN pip install --trusted-host pypi.python.org flask

####
#### OPTIONAL : 4. SET JAVA_HOME environment variable, uncomment the line below if you need it

#ENV JAVA_HOME="/usr/lib/jvm/java-1.8-openjdk"

####

EXPOSE 80    
ADD app.py /
CMD ["python", "app.py"]