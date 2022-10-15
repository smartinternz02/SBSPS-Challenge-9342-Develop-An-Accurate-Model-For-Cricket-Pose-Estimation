#!/usr/bin/env python
# coding: utf-8

# In[1]:


from ibm_watson_machine_learning import APIClient
wml_credentials={
    "url":"https://us-south.ml.cloud.ibm.com",
    "apikey":"tJxpvrqFLqoZt_x5PErYhOMhGHYfrGvrZjYdsHfrm9xf"
}


# In[2]:


client=APIClient(wml_credentials)
client


# In[3]:


def uid_space_name(client,Cricket_deploy):
    space=client.spaces.get_details()
    return(next(item for item in space['resources'] if item['entity']['name']==Cricket_deploy)['metadata']['id'])


# In[4]:


space_uid=uid_space_name(client,'Cricket_Pose_Classification')
print(space_uid)


# In[5]:


client.set.default_space(space_uid)


# In[6]:


client.repository.download('e5268ec5-890a-4c80-8460-2d07445de608','cricketcnn1.tgz')

