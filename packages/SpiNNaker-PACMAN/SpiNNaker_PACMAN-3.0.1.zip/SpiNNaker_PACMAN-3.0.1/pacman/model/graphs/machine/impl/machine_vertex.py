from pacman.model.abstract_classes.impl.constrained_object \
    import ConstrainedObject
from pacman.model.decorators.delegates_to import delegates_to
from pacman.model.decorators.overrides import overrides
from pacman.model.graphs.machine.abstract_machine_vertex \
    import AbstractMachineVertex


class MachineVertex(AbstractMachineVertex):
    """ A simple implementation of a machine vertex
    """

    __slots__ = [

        # The resources required
        "_resources_required",

        # The label
        "_label",

        # The constraints delegate
        "_constraints"
    ]

    def __init__(self, resources_required, label=None, constraints=None):
        """
        :param resources_required:\
            The maximum resources needed for the vertex
        :type resources_required:\
            :py:class:`pacman.models.resources.resource_container.ResourceContainer`
        :param label: The optional name of the vertex
        :type label: str
        :param constraints: The optional initial constraints of the vertex
        :type constraints: \
            iterable of\
            :py:class:`pacman.model.constraints.abstract_constraint.AbstractConstraint`
        :raise pacman.exceptions.PacmanInvalidParameterException:
                    * If one of the constraints is not valid
        """
        self._resources_required = resources_required
        self._label = label

        AbstractMachineVertex.__init__(self)
        self._constraints = ConstrainedObject(constraints)

    @delegates_to("_constraints", ConstrainedObject.add_constraint)
    def add_constraint(self, constraint):
        pass

    @delegates_to("_constraints", ConstrainedObject.add_constraints)
    def add_constraints(self, constraints):
        pass

    @delegates_to("_constraints", ConstrainedObject.constraints)
    def constraints(self):
        pass

    @property
    @overrides(AbstractMachineVertex.label)
    def label(self):
        return self._label

    @property
    @overrides(AbstractMachineVertex.resources_required)
    def resources_required(self):
        return self._resources_required

    def __str__(self):
        return self._label

    def __repr__(self):
        return (
            "MachineVertex(resources_required={}, label={}, constraints={}"
            .format(self._resources_required, self._label, self.constraints))
