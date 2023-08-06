// -*- coding: utf-8 -*-
//-----------------------------------------------------------------------------
// file: $Id$
// auth: Philip J Grabner <phil@canary.md>
// date: 2016/10/09
// copy: (C) Copyright 2016-EOT Canary Health, Inc., All Rights Reserved.
//-----------------------------------------------------------------------------

function (nodeid, baseurl, channels) {
  $(function() {
    var node = $('#' + nodeid);
    var stat = {inline: $.Deferred().resolve()};
    var indexOf = function(array, value) {
      for ( var idx=0 ; idx<array.length ; idx++ ) {
        if ( value === array[idx] )
          return idx;
      }
      return -1;
    }
    var loader = {
      load : function(channel, path) {
        if ( channel == 'jit' )
          channel = channel + '/' + ( path || '' );
        else if ( path !== undefined )
          return $.Deferred().reject('only "jit" channel supports parameters').promise();
        if ( stat[channel] )
          return stat[channel].promise();
        else if ( indexOf(channels, channel) < 0 )
          return $.Deferred().reject('no-such-channel: ' + channel).promise();
        var def = stat[channel] = $.Deferred();
        $.get(baseurl + '/' + channel).then(function(data) {
          node.append(data);
          def.resolve(channel);
        }, function(xhr, status, error) {
          def.reject({
            channel : channel,
            status  : status,
            error   : 'failed loading jitt channel "' + channel + '": ' + error,
            xhr     : xhr
          });
        });
        return def.promise();
      },
      unload : function(channel) {
        // todo: implement this...
        return $.Deferred().reject('NotImplementedError').promise();
      },
      ready : function(callback) {
        if ( indexOf(channels, 'deferred') < 0 )
          return loader.load('inline').then(callback);
        return loader.load('deferred').then(callback);
      }
    };
    node.data('jitt', loader);
    if ( indexOf(channels, 'deferred') >= 0 ) {
      loader.load('deferred').fail(function(error) {
        console.error(error.error);
      });
    }
  });
}

//-----------------------------------------------------------------------------
// end of $Id$
// $ChangeLog$
//-----------------------------------------------------------------------------
