/*
 * Copyright 2016 Flowdas Inc. <prospero@flowdas.com>
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */
#include "engine.h"

#define FD_EVENT_MASK (FM_READ|FM_WRITE)

int fm_start(struct fm_queue_t* queue, int interval)
{
    queue->kq = kqueue();

    if (queue->kq == -1) {
        return -1;
    }

    if (interval > 0 && queue->on_tick) {
        struct kevent change;

        EV_SET(&change, 0, EVFILT_TIMER, EV_ADD, NOTE_NSECONDS | NOTE_CRITICAL, interval, NULL);
        if (kevent(queue->kq, &change, 1, NULL, 0, NULL) == -1) {
            close(queue->kq);
            queue->kq = -1;
            return -1;
        }
    }

    return 0;
}

int fm_stop(struct fm_queue_t* queue)
{
    int rc = 0;
    if (queue->kq != -1) {
        rc = close(queue->kq);
        queue->kq = -1;
    }
    return rc;
}

int fm_execute(struct fm_queue_t* queue)
{
    struct kevent event;
    int rc;

    rc = kevent(queue->kq, NULL, 0, &event, 1, NULL);
    if (rc < 0) {
        return -1;
    }
    if (rc == 1) {
        switch(event.filter) {
            case EVFILT_TIMER:
                return (*queue->on_tick)(queue, event.data);
            case EVFILT_READ:
                if (queue->on_read) {
                    return (*queue->on_read)(queue, (struct fm_socket_t*)event.udata);
                }
                break;
            case EVFILT_WRITE:
                if (queue->on_write) {
                    return (*queue->on_write)(queue, (struct fm_socket_t*)event.udata);
                }
                break;
        }
    }
    return 0;
}

int fm_attach(struct fm_queue_t* queue, struct fm_socket_t* socket, int events)
{
    socket->events = 0;
    return fm_set_events(queue, socket, events);
}

int fm_detach(struct fm_queue_t* queue, struct fm_socket_t* socket)
{
    return fm_set_events(queue, socket, 0);
}

int fm_set_events(struct fm_queue_t* queue, struct fm_socket_t* socket, int events)
{
    struct kevent changes[2];
    int nchanges = 0;
    int flags;
    int rc;

    int diffs = (FD_EVENT_MASK & events) ^ socket->events;
    if (diffs == 0) {
        return 0;
    }
    if (diffs & FM_READ) {
        flags = (events & FM_READ) ? EV_ADD : EV_DELETE;
        EV_SET(changes+nchanges, socket->sd, EVFILT_READ, flags, 0, 0, socket);
        nchanges++;
    }
    if (diffs & FM_WRITE) {
        flags = (events & FM_WRITE) ? EV_ADD : EV_DELETE;
        EV_SET(changes+nchanges, socket->sd, EVFILT_WRITE, flags, 0, 0, socket);
        nchanges++;
    }
    rc = kevent(queue->kq, changes, nchanges, NULL, 0, NULL);
    if (rc != -1) {
        socket->events ^= diffs;
    }
    return rc;
}

int fm_get_events(struct fm_queue_t* queue, struct fm_socket_t* socket)
{
    return socket->events;
}
