FROM gradle
RUN echo "hi" > artifact
FROM tomcat
CMD ["/bin/bash"]