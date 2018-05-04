FROM neungkl/ml-utility

RUN pip3 install jupyterlab

RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/* /root/.cache/pip/

CMD ["jupyter", "lab", "--allow-root"]