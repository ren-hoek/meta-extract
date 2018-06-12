docker run -d \
	-v /etc/passwd:/etc/passwd \
	-v /etc/shadow:/etc/shadow \
	-v /etc/group:/etc/group \
	-v /etc/gshadow:/etc/gshadow \
	-v /home:/home \
	-e USER=$(whoami) \
	-p 8888:8888 \
	--name jpytika \
	--hostname jpytika \
	--network jupyterhub \
	analysis/tika-notebook

