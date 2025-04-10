# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from abc import abstractmethod
from enum import Enum
from typing import Optional, Dict

from gravitino.api.auditable import Auditable


class Fileset(Auditable):
    """An interface representing a fileset under a schema Namespace. A fileset is a virtual
    concept of the file or directory that is managed by Gravitino. Users can create a fileset object
    to manage the non-tabular data on the FS-like storage. The typical use case is to manage the
    training data for AI workloads. The major difference compare to the relational table is that the
    fileset is schema-free, the main property of the fileset is the storage location of the
    underlying data.

    Fileset defines the basic properties of a fileset object. A catalog implementation
    with FilesetCatalog should implement this interface.
    """

    class Type(Enum):
        """An enum representing the type of the fileset object."""

        MANAGED = "managed"
        """Fileset is managed by Gravitino. 
        When specified, the data will be deleted when the fileset object is deleted"""

        EXTERNAL = "external"
        """Fileset is not managed by Gravitino. 
        When specified, the data will not be deleted when the fileset object is deleted"""

    @abstractmethod
    def name(self) -> str:
        """
        Returns:
            Name of the fileset object.
        """
        pass

    @abstractmethod
    def comment(self) -> Optional[str]:
        """
        Returns:
            The comment of the fileset object. Null is returned if no comment is set.
        """
        pass

    @abstractmethod
    def type(self) -> Type:
        """
        @Returns:
            The type of the fileset object.
        """
        pass

    @abstractmethod
    def storage_location(self) -> str:
        """Get the storage location of the file or directory path managed by this fileset object.

        The returned storageLocation can be either the one specified when creating the fileset object,
        or the one specified at the catalog/schema level if the fileset object is created under this
        catalog/schema.

        The storageLocation at each level can contain placeholders, formatted as {{name}}, which will
        be replaced by the corresponding fileset property value when the fileset object is created.
        The placeholder property in the fileset object is formed as "placeholder-{{name}}". For example,
        if the storageLocation is "file:///path/{{schema}}-{{fileset}}-{{version}}", and the fileset
        object "catalog1.schema1.fileset1" has the property "placeholder-version" set to "v1",
        then the storageLocation will be "file:///path/schema1-fileset1-v1".

        For managed fileset, the storageLocation can be:

        1) The one specified when creating the fileset object, and the placeholders in the
           storageLocation will be replaced by the placeholder value specified in the fileset properties.

        2) When catalog property "location" is specified but schema property "location" is not specified,
           then the storageLocation will be:
            a. "{catalog location}/schemaName/filesetName" - if {catalog location} has no placeholders
            b. "{catalog location}" - placeholders in {catalog location} will be replaced by values
               specified in fileset properties

        3) When catalog property "location" is not specified but schema property "location" is specified,
           then the storageLocation will be:
            a. "{schema location}/filesetName" - if {schema location} has no placeholders
            b. "{schema location}" - placeholders in {schema location} will be replaced by values
               specified in fileset properties

        4) When both catalog property "location" and schema property "location" are specified,
           then the storageLocation will be:
            a. "{schema location}/filesetName" - if {schema location} has no placeholders
            b. "{schema location}" - placeholders in {schema location} will be replaced by values
               specified in fileset properties

        5) When both catalog property "location" and schema property "location" are not specified,
           and storageLocation specified when creating the fileset object is null, this situation
           is illegal.

        For external fileset, the storageLocation can be:
        1) The one specified when creating the fileset object, and the placeholders in the
           storageLocation will be replaced by the placeholder value specified in the fileset properties.

        Returns:
            str: The storage location of the fileset object.
        """
        pass

    @abstractmethod
    def properties(self) -> Dict[str, str]:
        """
        Returns:
            The properties of the fileset object. Empty map is returned if no properties are set.
        """
        pass
