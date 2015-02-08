import lib
import model

class IndexPage(lib.BaseHandler):
  def get(self):
    template_values = self.GetTemplateValues()
    if self.user:
      q = model.Mapping.all()
      q.filter("owner =", self.user)
      q.filter("deleted =", False)
      template_values['mappings'] = q
    self.RenderTemplate("index.html", template_values)
