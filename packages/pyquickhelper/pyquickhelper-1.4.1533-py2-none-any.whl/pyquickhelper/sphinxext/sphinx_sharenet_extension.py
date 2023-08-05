# -*- coding: utf-8 -*-
"""
@file
@brief Defines a sphinx extension to add button to share a page

.. versionadded:: 1.3
"""
from __future__ import unicode_literals
import sphinx
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.writers.html import HTMLTranslator


class sharenet_node(nodes.Structural, nodes.Element):

    """
    defines *sharenet* node
    """
    pass


class ShareNetDirective(Directive):
    """
    Adds buttons to share a page. It can be done by
    adding::

        .. sharenet::
            :facebook: 1
            :linkedin: 2
            :twitter: 3
            :head: False

    Which gives:

    .. sharenet::
        :facebook: 1
        :linkedin: 2
        :twitter: 3
        :head: False

    The integer indicates the order in which they need to be displayed.
    It is optional. The option ``:head: False`` specifies the javascript
    part is added to the html body and not the header.
    The header can be overwritten by other custom commands.
    """
    available_networks = {'facebook', 'linkedin', 'twitter'}
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {'facebook': directives.unchanged,
                   'linkedin': directives.unchanged,
                   'twitter': directives.unchanged,
                   'size': directives.unchanged,
                   'head': directives.unchanged,
                   }
    has_content = True
    sharenet_class = sharenet_node

    def run(self):
        """
        extracts the information in a dictionary,
        run the script

        @return      a list of nodes
        """
        def options_to_int(s):
            if s is None:
                return -1
            elif len(s) == 0:
                return 1e6
            else:
                return int(s)

        # list of networks
        bool_set = (True, 1, "True", "1", "true")
        p = [(options_to_int(self.options.get(net, None)), net)
             for net in ShareNetDirective.available_networks]
        p.sort()
        p = [a[1] for a in p if a[0] >= 0]

        # build node
        node = self.__class__.sharenet_class(networks=p,
                                             size=self.options.get('size', 20),
                                             inhead=self.options.get('head', True) in bool_set)
        node['classes'] += "-sharenet"
        node['sharenet'] = node
        ns = [node]
        return ns


def sharenet_role(role, rawtext, text, lineno, inliner,
                  options={}, content=[]):
    """
    Defines custom roles *sharenet*. The following instructions defines
    buttons of size 20 (:sharenet:`facebook-linkedin-twitter-20-body`)::

        :sharenet:`facebook-linkedin-twitter-20-body`

    The last term indicates the javascript part will be included in the
    HTML body instead of the head as this part might be tweaked by other
    custom commands.

    :param name: The role name used in the document.
    :param rawtext: The entire markup snippet, with role.
    :param text: The text marked with the role.
    :param lineno: The line number where rawtext appears in the input.
    :param inliner: The inliner instance that called us.
    :param options: Directive options for customization.
    :param content: The directive content for customization.
    """
    spl = [a.strip().lower() for a in text.split('-')]
    networks = []
    size = 20
    inhead = True
    for v in spl:
        if v in ShareNetDirective.available_networks:
            networks.append(v)
        elif v == "body":
            inhead = False
        elif v == "head":
            inhead = True
        else:
            try:
                i = int(v)
                size = i
            except ValueError:
                msg = inliner.reporter.error(
                    "unable to interpret {0} from {1}".format(v, rawtext), line=lineno)
                prb = inliner.problematic(rawtext, rawtext, msg)
                return [prb], [msg]

    if len(networks) == 0:
        msg = inliner.reporter.error(
            "no specified network from {0}".format(rawtext), line=lineno)
        prb = inliner.problematic(rawtext, rawtext, msg)
        return [prb], [msg]

    # ref = inliner.document.settings.rfc_base_url + inliner.rfc_url % rfcnum
    # set_classes(options)
    node = sharenet_node(networks=networks, size=size, inhead=inhead)
    node['classes'] += "-sharenet"
    node['sharenet'] = node
    return [node], []


def visit_sharenet_node(self, node):
    """
    what to do when visiting a node sharenet
    the function should have different behaviour,
    depending on the format, or the setup should
    specify a different function for each.
    """
    pass


def depart_sharenet_node(self, node):
    """
    what to do when leaving a node sharenet
    the function should have different behaviour,
    depending on the format, or the setup should
    specify a different function for each.

    It does only html for the time being.
    """
    if not isinstance(self, HTMLTranslator):
        self.body.append("%sharenet: output only available for HTML\n")
        return

    if node.hasattr("networks"):
        networks = node["networks"]
        size = node["size"]
        inhead = node["inhead"]
        if len(networks) > 0:

            script = """
                        <script>
                        function share_url(share) {
                            var url = share + encodeURIComponent(window.location.href);
                            window.location.href = url;
                        }

                        function share_icon(divid, text) {
                            var canvas = document.getElementById(divid);
                            var context = canvas.getContext('2d');
                            var centerX = canvas.width / 2;
                            var centerY = canvas.height / 2;
                            var radius = centerX;

                            context.beginPath();
                            context.arc(centerX, centerY, radius, 0, 2 * Math.PI, false);
                            context.fillStyle = '#444444';
                            context.fill();
                            context.font = '' + (centerX*4/3) + 'pt Calibri';
                            context.textAlign = 'center';
                            context.fillStyle = '#FFFFFF';
                            context.fillText(text, centerX, centerY+centerY*16/30);
                        }
                        </script>
                        """.replace("                        ", "")

            mapping = dict(facebook="f", linkedin="in", twitter="t")
            urls = dict(facebook="https://www.facebook.com/sharer/sharer.php?u=",
                        twitter="https://twitter.com/home?status=",
                        linkedin="https://www.linkedin.com/shareArticle?mini=true&amp;title=&amp;summary=&amp;source=&amp;url=")
            link = """<a href="#" onclick="share_url('{0}');return false;"><canvas height="{2}" id="canvas-{1}" width="{2}"/>""" + \
                   """</a><script>share_icon('canvas-{1}', '{1}');</script>"""

            rows = []
            for key in networks:
                text = mapping[key]
                l = link.format(urls[key], text, size)
                rows.append(l)

            if len(rows) > 0:
                if inhead:
                    self.head.append(script)
                else:
                    self.body.append(script)
                self.body.extend(rows)


def setup(app):
    """
    setup for ``sharenet`` (sphinx)
    """
    if hasattr(app, "add_mapping"):
        app.add_mapping('sharenet', sharenet_node)

    app.add_config_value('sharepost', None, 'env')

    app.add_node(sharenet_node,
                 html=(visit_sharenet_node, depart_sharenet_node),
                 latex=(visit_sharenet_node, depart_sharenet_node),
                 text=(visit_sharenet_node, depart_sharenet_node))

    app.add_directive('sharenet', ShareNetDirective)
    app.add_role('sharenet', sharenet_role)
    return {'version': sphinx.__display_version__, 'parallel_read_safe': True}
