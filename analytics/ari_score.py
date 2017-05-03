
# coding: utf-8

# In[21]:

from sklearn.metrics import adjusted_rand_score
import pandas as pd


# In[93]:

joint = pd.read_csv("output/joint_total_node_intid.csv",header=None, names=["addr","user"] )
serial  = pd.read_csv("output/serial_total_node_intid.csv",header=None, names=["addr","user"])
joint_n_serial = pd.read_csv("output/joint_serial_total_node_intid.csv",header=None, names=["addr","user"])
kmeans = pd.read_csv("output/kmeans_node.csv",header=None, names=["addr","user"])


# In[94]:

joint.sort_values("addr", inplace=True)
serial.sort_values("addr", inplace=True)
joint_n_serial.sort_values("addr", inplace=True)
kmeans.sort_values("addr", inplace=True)


# In[95]:

pd.value_counts(pd.Series(kmeans.addr))


# In[96]:

kmeans.drop(kmeans.index[kmeans.addr==[1774115477]], axis = 0, inplace=True)
kmeans.drop(kmeans.index[kmeans.addr==[1607992254]], axis = 0, inplace=True)
kmeans


# In[97]:

joint.drop(joint.index[joint.addr==[1774115477]], axis = 0, inplace=True)
joint.drop(joint.index[joint.addr==[1607992254]], axis = 0, inplace=True)
joint


# In[98]:

serial.drop(serial.index[serial.addr==[1774115477]], axis = 0, inplace=True)
serial.drop(serial.index[serial.addr==[1607992254]], axis = 0, inplace=True)
serial


# In[99]:

joint_n_serial.drop(joint_n_serial.index[joint_n_serial.addr==[1774115477]], axis = 0, inplace=True)
joint_n_serial.drop(joint_n_serial.index[joint_n_serial.addr==[1607992254]], axis = 0, inplace=True)
joint_n_serial


# In[100]:

adjusted_rand_score(joint.user,serial.user)


# In[101]:

adjusted_rand_score(joint_n_serial.user,serial.user)


# In[102]:

adjusted_rand_score(joint_n_serial.user,joint.user)


# # K-means vs Others

# In[103]:

adjusted_rand_score(kmeans.user,serial.user)


# In[104]:

adjusted_rand_score(kmeans.user,joint.user)


# In[105]:

adjusted_rand_score(kmeans.user,joint_n_serial.user)


# In[ ]:



