Docker Image naming:
 - sementic_version + SHA commit 
 - by default it is latest, which is not a good practice. 


Creating a replicated application:
 - On kubernetes it is a good practice to use deployment instead of replica set. 
 -deployment includes RS capabilities with versioning and ability to perform staged rollout. 
 
  