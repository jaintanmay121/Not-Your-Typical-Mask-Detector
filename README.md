# Not Your Typical Mask Detector

This is an **Extended Version** of the typical mask detector. 

This project initially is the same as the other mask detection projects, however after checking for a mask, if a person is not wearing a mask, it uses face recognition to identify the person and gets his details from the **PostgreSQL** database and e-mails him/her an acknowledgement for it.

Working Video: https://www.linkedin.com/feed/update/urn:li:activity:6693812186780905472/

`Note: You could use a SQLite database too, which will be much easier, since you won't need to install postgres on your machine.`

<img alt="Description" width="700" height='800' src="Mask Project Flow.jpg">
