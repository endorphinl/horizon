/*
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
(function () {
  'use strict';

  angular
    .module('horizon.framework.util.tech-debt')
    .controller('hzModalFormUpdateMetadataController', hzModalFormUpdateMetadataController);

  hzModalFormUpdateMetadataController.$inject = ['$scope', '$window'];

  function hzModalFormUpdateMetadataController($scope, $window) {
    var ctrl = this;

    ctrl.tree = null;
    ctrl.available = $window.available_metadata.namespaces;
    ctrl.existing = $window.existing_metadata;

    ctrl.saveMetadata = function () {
      var metadata = [];
      angular.forEach(ctrl.tree.getExisting(), function (value, key) {
        metadata.push({
          key: key,
          value: value

        });

      });

      ctrl.metadata = angular.toJson(metadata);

    };

  }

}());
