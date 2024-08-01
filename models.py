class Job:
  def __init__(self, id, company, title, url, recruiter, timestamp):
    self.id = id
    self.company = company
    self.title = title
    self.url = url
    self.recruiter = recruiter
    self.timestamp = timestamp

  def __repr__(self):
    return '<id {}>'.format(self.id)

  def serialize(self):
    return {
      'id': self.id,
      'company': self.company,
      'title': self.title,
      'url': self.url,
      'recruiter': self.recruiter,
      'timestamp':self.timestamp
    }