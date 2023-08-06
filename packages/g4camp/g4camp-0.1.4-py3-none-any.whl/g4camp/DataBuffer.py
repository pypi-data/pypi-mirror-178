import numpy as np

class Track():

  def __init__(self, unique_id, parent_id, pdg_id):
    self.unique_id = unique_id
    self.parent_id = parent_id
    self.pdg_id = pdg_id
    self.points = []

  def __str__(self):
    return f"UID: {self.unique_id},  parent_ID: {self.parent_id},  PDGID: {self.pdg_id}\n" + \
           f"points:\n" + \
           f"  {self.points[0]}\n" + \
           f"  ... \n" + \
           f"  {self.points[-1]}\n"

  def __repr__(self):
    return self.__str__()

  def AddPoint(self, point):
    self.points.append(point)
    pass



class DataBuffer():

  def __init__(self):
    self.vertices = []
    #
    self.track_points_per_bunch = 100000
    self.track_point_bunches = 1
    self.point_num = 0
    self.tracks = np.zeros((self.track_points_per_bunch, 7), dtype=float) 
    # 'track' row:  uid, pdgid, x[m], y[m], z[m], t[ns], Etot[GeV]
    self.photon_cloud = []
    self.status = 'empty' # 'empty' -> 'in_progress' -> 'ready'

  def AddVertex(self, vertex):
    self.status = 'in_progress'
    self.vertices.append(vertex)

  def AddPhoton(self, photon):
    self.status = 'in_progress'
    self.photon_cloud.append(photon)

  def CreateTrack(self, uid, parent_id, pdg_id):
    pass
#    self.status = 'in_progress'
#    self.tracks[uid] = Track(uid, parent_id, pdg_id)

  def AddTrackPoint(self, uid, pdgid, x, y, z, t, Etot):
    self.tracks[self.point_num] = [uid, pdgid, x, y, z, t, Etot]
    self.point_num += 1
    if self.point_num % self.track_points_per_bunch == 0:
      self.tracks = np.concatenate((self.tracks, np.zeros((self.track_points_per_bunch, 7), dtype=int)))
      self.track_point_bunches += 1

  def CutEmptyTrackPoints(self):
    self.tracks = self.tracks[:self.point_num]

  def SortTrackPoints(self):
    self.tracks = self.tracks[np.lexsort((self.tracks[:,5], self.tracks[:,0]))]

  def Clear(self):
    self.__init__()

  def Close(self):
    self.status = 'ready'

  def IsEmpty(self):
    return self.status == 'empty'

  def IsReady(self):
    return self.status == 'ready'

